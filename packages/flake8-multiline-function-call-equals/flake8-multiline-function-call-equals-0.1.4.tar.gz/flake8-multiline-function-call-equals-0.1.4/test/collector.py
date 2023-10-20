'''
Abstract base class for the collection of social media data
'''
import inspect
import json
import operator
import os
import datetime
import logging
from abc import ABC, abstractmethod

import pytz

from SocialCollector import lib


class Collector(ABC):

    @abstractmethod
    def __init__(self, type='p', cli=None, output_header=None):
        '''
        Initialize the Collector. This method should set up the logger, output file,
        and column header.

        Collectors using Selenium as their base should additionally have an error
        output file - see fbcollector.py for implementation

        Parameters
        ----------
        type : char
            p: Collect all posts from a list of channel URLs
            c: Collect channel information from a list of channel URLs
            r: Collect post data from a list of previously collected posts (aka 'retrospective')
            other: will generate an error
        cli : argparse.Namespace
             the commandline arguments passed to this collector
        output_header : list (default None)
            List of column names for output, if not using the built in column headers
        '''
        super().__init__()

        self.logger = logging.getLogger('Collector')
        self.column_header = NotImplemented
        self.output_file = NotImplemented
        self.path = NotImplemented

        self.platform = NotImplemented
        self.type = NotImplemented
        self.cli = NotImplemented

        self.page_list = NotImplemented

        self.timezone = pytz.utc
        self.collection_date = datetime.datetime.now(tz=self.timezone)
        self.collection_str = self.collection_date.strftime('%Y-%b-%dT%H-%M')

    ''' SETUP '''
    @abstractmethod
    def setup_logger(self, name=None):
        '''
        Default set up for debug and error handlers
        Assumes self.logger has already been created

        Set the logger's name to `name`. If None, the name is not changed
        '''

        if self.logger == NotImplemented:
            raise NotImplementedError

        logs_dir = os.path.join(self.path, 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(os.path.join(logs_dir, 'log'),
                                                       maxBytes = 10**6,
                                                       backupCount = 5,
                                                       )

        handler.setFormatter(logging.Formatter('{levelname} | {lineno} | {asctime} || {message}',
                                               style = '{',
                                               )
                             )
        self.logger.addHandler(handler)
        if name is not None:
            self.logger.name = name

    def check_start_and_end_date(self, page, default_start=7):
        '''
            If start date (aka earliest post to collect) is not set in the page data,
            start date will be set to 7 days ago (aka a week of data)
            If end date (aka latest post to collect) is not set, end date will be set to today
            Start and end dates are inclusive

            Parameters
            ----------
            page : dict
                Dict of data about the post to collect
            default_start : int (default 7)
                How many days back to look for posts if Start Date is not set in original file

            Returns
            -------
            start_date, end_date : date
                Tuple with the date objects representing the start and end date

        '''

        start_date = page.get('Start Date')
        end_date = page.get('End Date')

        if start_date is None:
            start_date = datetime.date.today() - datetime.timedelta(days=default_start)
        else:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date is None:
            end_date = datetime.date.today()
        else:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        return start_date, end_date

    def write_to_db(self, cur, update_id, row):
        """
        Write the information in `row` to the database.
        This is a generic swiss-army-knife function that imputes a missing channel/post
        and handles fetching all the necessary foreign keys

        :param cur: database cursor
        :param row: the dict with the data to be written
        :return: dict - subset of the k,v pairs in row that were not written to the database
        """

        self.logger.debug(f'Update {update_id}: data {row}')

        row['measurement_time'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        row['platform'] = row['platform_id'] = self.platform
        row['update_id'] = update_id

        if 'qbit_error_code' in row:  # error signal

            error = row['qbit_error_code']
            row['qbit_error_code'] = error.name
            row['qbit_error_description'] = error.value

            get_measurement_id = """
                                SELECT COALESCE(max(measurement_id), 0)+1 as answer
                                FROM updates.missing
                                WHERE update_id = %s
                                 """
            cur.execute(get_measurement_id, (update_id,))
            measurement_id = cur.fetchone().answer

            query = f"""
                    INSERT INTO updates.missing(update_id, measurement_name, measurement_value, measurement_time, measurement_id)
                    VALUES({update_id}, %s, %s, %s, %s)
                    """

            for row['measurement_name'], measurement_value in {**row}.items():
                measurement_value = {False: None, True: measurement_value}[bool(measurement_value)]

                if isinstance(measurement_value, datetime.datetime):
                    measurement_value = measurement_value.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    measurement_value = json.dumps(measurement_value)
                except Exception as e:
                    self.logger.error(f"Could not convert {row['measurement_name']} with value {measurement_value} to JSON\n{e}")

                row['measurement_value'] = json.dumps(measurement_value)

                cur.execute(query, (row['measurement_name'], row['measurement_value'], row['measurement_time'], measurement_id))
                cur.connection.commit()

            return

        insert_channel = f"""
                            INSERT INTO objects.channels
                                    (platform_id, {'group_id,' if 'group_id' in row else ''} source_id, creation_date)
                            VALUES 
                                    (%(platform)s, {'% (group)s,' if 'group_id' in row else ''} %(source)s, %(creation)s)
                            """

        if self.type in (lib.CollecTypes.retrospective,
                         lib.CollecTypes.posts,
                         lib.CollecTypes.last_post,
                         ) or row.get('table') == 'posts':  # post collections

            channel_source_id = row.get('channel_source_id', row.get('source_id'))

            get_channel_id = f"""
                             SELECT id from objects.channels
                             WHERE source_id = %s :: varchar
                               AND platform_id = %s
                             """
            cur.execute(get_channel_id, (channel_source_id, row['platform']))
            channel_id = cur.fetchone()
            if channel_id is None:  # the channel doesn't yet exist in the database. Insert it first
                cur.execute(insert_channel,
                            dict(platform = row['platform'],
                                 source = channel_source_id,
                                 creation = row['measurement_time'],
                                 **(dict(group=row['group_id']) if 'group_id' in row else {}),
                                 ),
                            )
                cur.connection.commit()

                cur.execute(get_channel_id, (channel_source_id, self.platform))  # the channel has been inserted. Get the ID now
                channel_id = cur.fetchone()

            row['channel_id'] = channel_id = getattr(channel_id, 'id', 0)

            get_post_id = """
                    SELECT id
                    FROM objects.posts
                    WHERE COALESCE(source_id, '') = COALESCE(%(source)s :: varchar, '')
                      AND channel_id = %(channel)s
                    """
            cur.execute(get_post_id,
                        dict(source = row['source_id'],
                             channel = row['channel_id'],
                             ),
                        )
            row['post_id'] = post_id = cur.fetchone()
            if post_id is None:  # the post does not yet exist in the database. Insert first

                query = f"""
                        INSERT INTO objects.posts(source_id, channel_id, url)
                                VALUES(%(source_id)s, %(channel)s, %(url)s)
                        """
                cur.execute(query,
                            dict(source_id = row['source_id'],
                                 channel = channel_id,
                                 url = row.get('url'),
                                 ),
                            )
                cur.connection.commit()

                # the post has been inserted. Get the ID now
                cur.execute(get_post_id,
                            dict(source = row['source_id'],
                                 channel = channel_id,
                                 ),
                            )

                row['post_id'] = cur.fetchone().id

            table = 'posts'

        elif self.type == lib.CollecTypes.comments:

            cur.execute(f"""
                        SELECT id from objects.comments
                        WHERE source_id = %s
                        """,
                        (row['source_id'],),
                        )
            comment_id = cur.fetchone()
            post_source_id = row['post_source_id']

            if comment_id is None:  # the comment doesn't exist in the database

                get_post_id = f"""
                              SELECT id from objects.posts
                              WHERE source_id = %s :: varchar
                              """
                cur.execute(get_post_id, (post_source_id,))
                post_id = cur.fetchone()
                if post_id is None:  # the post doesn't exist in the database
                    channel_source_id = row['channel_source_id']
                    cur.execute(f"""
                                SELECT id from objects.channels
                                WHERE source_id = %s :: varchar
                                """,
                                (channel_source_id,)
                                )
                    channel_id = cur.fetchone()
                    if channel_id is None:  # the channel doesn't exist in the database
                        cur.execute(insert_channel,
                                    dict(platform = row['platform'],
                                         source = channel_source_id,
                                         creation = row['measurement_time'],
                                         **(dict(group=row['group_id']) if 'group_id' in row else {}),
                                         ),
                                    )

                        get_channel_id = f"""
                                         SELECT id from objects.channels
                                         WHERE source_id = %s :: varchar
                                         """

                        cur.execute(get_channel_id, (channel_source_id,))  # the channel has been inserted. Get the ID now
                        channel_id = cur.fetchone()

                    row['channel_id'] = channel_id

                    cur.execute(f"""
                                INSERT INTO objects.posts(source_id, channel_id)
                                VALUES (%(source_id)s, %(channel)s)
                                """,
                                dict(source_id = post_source_id,
                                     channel = channel_id,
                                     ),
                                )

                cur.execute(f"""
                            SELECT id from objects.posts
                            WHERE source_id = %s :: varchar
                            """,
                            (row['post_source_id'],),
                            )
                post_id = cur.fetchone().id

                cur.execute(f"""
                            INSERT INTO objects.comments (source_id, post_id)
                            VALUES (%s, %s)
                            """,
                            (row['source_id'], post_id),
                            )

                cur.execute(f"""
                            SELECT id from objects.comments
                            WHERE source_id = %s
                            """,
                            (row['source_id'],),
                            )
                comment_id = cur.fetchone()

            row['comment_id'] = comment_id.id

            cur.execute(f"""
                        SELECT id from objects.posts
                        WHERE source_id = %s :: varchar
                        """,
                        (post_source_id,),
                        )
            row['post_id'] = cur.fetchone().id  # the post has been inserted. Get the ID now

            table = 'comments'

        elif self.type == lib.CollecTypes.channels or row.get('table') == 'channels':
            get_channel_id = f"""
                             SELECT id from objects.channels
                             WHERE source_id = %s :: varchar
                             """
            cur.execute(get_channel_id, (row['source_id'],))

            channel_id = cur.fetchone()
            if channel_id is None:  # the channel does not yet exist in the database. Insert it first
                cur.execute(insert_channel,
                            dict(platform = row['platform'],
                                 source = row.get('source_id', None),
                                 creation = row['measurement_time'],
                                 **(dict(group=row['group_id']) if 'group_id' in row else {}),
                                 ),
                            )
                cur.connection.commit()

                cur.execute(get_channel_id, (row['source_id'],))
                channel_id = cur.fetchone()

            channel_id = row['channel_id'] = channel_id.id
            table = 'channels'

        query = """
        SELECT measurement_name
        FROM config.platforms as list
        INNER JOIN config.platform_property as prop
                ON list.id = prop.platform_id
        WHERE prop.platform_id = %s
        """
        cur.execute(query, (self.platform,))
        measurements = set(q for (q,) in cur)

        unwritten = {}
        query = f"""
                SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE table_name = %s
                  AND table_schema = 'updates'
                """
        cur.execute(query, (table,))
        colnames = {p for (p,) in cur if not p.startswith('tag_')}  # channels have an associated tag_id
        prop_getter = operator.itemgetter(*colnames)

        language_getter = f"""
                            SELECT id
                            FROM objects.languages
                            WHERE google_code = %s
                          """

        query = f"""
                INSERT INTO updates.{table} 
                    ({', '.join(colnames)})

                VALUES 
                    ({', '.join(['%s'] * (len(colnames)) )})
                """

        if self.type == lib.CollecTypes.channels:
            get_last_post = f"""
                             SELECT max(CASE
                                         WHEN measurement_value = 'null'
                                             THEN NULL
                                         WHEN measurement_value::varchar LIKE '%T%'
                                             THEN to_timestamp(BTRIM(measurement_value::varchar, '"'), 'YYYY-MM-DDTHH24:MI:SSZ')
                                         ELSE to_timestamp(BTRIM(measurement_value::varchar, '"'), 'YYYY-MM-DD HH24:MI:SS+TZM')
                                        END
                                        ) as last_post_time
                             FROM updates.posts
                             WHERE channel_id = {channel_id}
                               AND measurement_name = 'publication_date_time'
                             """
            cur.execute(get_last_post)
            try:
                row['most_recent_post_date'] = cur.fetchone().last_post_time
            except AttributeError:
                self.logger.warning('Most recent post not found')

        for measurement_name, row['measurement_value'] in {**row}.items():  # don't change `row` as you iterate over it
            if measurement_name not in measurements:
                unwritten[measurement_name] = row['measurement_value']
                continue

            row['measurement_name'] = measurement_name
            if measurement_name == 'language' and not row['language']:
                googlang = row['measurement_value']
                cur.execute(language_getter, (googlang,))
                try:
                    row['measurement_value'] = cur.fetchone().id
                except AttributeError:
                    self.logger.warning('Language not found')

            values = prop_getter(row)
            values = [{False: None, True: v}[bool(v)] for v in values]
            for i, (k, v) in enumerate(zip(prop_getter.__reduce__()[1], values)):
                if k == 'measurement_value':
                    if isinstance(v, datetime.datetime) or isinstance(v, datetime.date):
                        v = v.strftime("%Y-%m-%d %H:%M:%S%z")
                    values[i] = json.dumps(v)
                    break
            values = tuple(values)

            cur.execute(query, values)
            cur.connection.commit()

        return unwritten

    def collect_retrospective(self):
        raise NotImplementedError

    def collect_comments(self):
        raise NotImplementedError

    def collect_posts(self):
        raise NotImplementedError

    def collect_channels(self):
        raise NotImplementedError

    def collect_last_post(self):
        raise NotImplementedError

    async def run_service(self, conf, qIn, qOut):
        """
        Given all the necessary config information, run the appropriate data collection methodology

        :param conf: A dictionary that contains all necessary config information. Expected keys include
            cursor: a cursor to the database into which data should be written
            update_id: an int signifying the update ID against which to write this information to the database
            AWS: a dict containing AWS credentials for media archiving
        :param qIn: an IPQ through which this collector will receive data to process
        :param qOut: an IPQ to which processed data will be written by this collector. This will be consumed by write_to_db
        :return: None
        """

        collectors = {lib.CollecTypes.retrospective: self.collect_retrospective,
                      lib.CollecTypes.comments: self.collect_comments,
                      lib.CollecTypes.posts: self.collect_posts,
                      lib.CollecTypes.channels: self.collect_channels,
                      lib.CollecTypes.last_post: self.collect_last_post,
                      }

        for row in iter(qIn.get, None):
            f = collectors[self.type]

            args = [row, conf['cursor'], conf['update_id']]
            if self.platform == lib.PLATFORM_ID.telegram.value:  # downloading media currently supported only for TG
                if self.type in (lib.CollecTypes.posts, lib.CollecTypes.last_post):
                    args.extend((conf.get('AWS'),))

            if inspect.iscoroutinefunction(f):
                await f(*args)
            else:
                f(*args)

        if self.platform == lib.PLATFORM_ID.telegram.value:
            await self.client.disconnect()  # the Telegram scraper populates this on __init__

        qOut.put(self.platform)
