import asyncio
import collections
import csv
import datetime as dt
import glob
import itertools
import logging
import multiprocessing as mp
import os
import shutil
import string
import sys
import tempfile

import psycopg2 as pg
import psycopg2.extras as pgex
import sentry_sdk
import traceback
import yaml
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk import Hub

from SocialCollector import lib
from SocialCollector.DriveAPI.drive import DriveService
from SocialCollector.Telegram.collector import Collector as TGCollector
# from SocialCollector.Twitter.collector import Collector as TWCollector
from SocialCollector.YouTube.collector import Collector as YTCollector
from SocialCollector.whatsapp.collector import Collector as WACollector
from SocialCollector.Reddit.collector import Collector as RDCollector


Collector = collections.namedtuple('Collector', "proc qIn")


class MasterCollector:
    '''
    This is the master, collection class that should manage all platform-level collectors
    '''

    def __init__(self, tgConfigPath, collectors, notes=None):
        """
        :param tgConfigPath: a config file with the API key/hash information for all available TG sessions.
                It is assumed that there are session files nearby as well.
                The tgConfig file contains a section for each session file that we might find
        """

        self.config = self.read_config(tgConfigPath)
        if not self.config['test_mode']:
            sentry_config = self.config['sentry']
            sentry_secret = sentry_config['secret']
            sentry_host = sentry_config['host']
            project_num = sentry_config['project_num']
            sentry_sdk.init(f"https://{sentry_secret}@{sentry_host}/{project_num}",
                            traces_sample_rate = 1.0,
                            integrations = [LoggingIntegration(level = 0,  # Capture info and above as breadcrumbs
                                                               event_level = logging.WARNING,  # Send warnings/above as events
                                                               ),
                                            ],
                            )

        self.log_dir = 'logs'
        os.makedirs(self.log_dir, exist_ok=True)

        logging.basicConfig(filename='logs/r')
        self.logger = logging.getLogger('MasterCollector')
        self.logger.setLevel(logging.DEBUG)

        config = self.config['database']
        update_start_time = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        with pg.connect(host=config['host'], database=config['db_name'], user=config['user'], password=config['pass']) as conn:
            conn.set_session(autocommit=True)
            with conn.cursor(cursor_factory=pgex.NamedTupleCursor) as cur:
                query = """
                        INSERT INTO updates.updates(start_time, notes) VALUES (%s, %s) RETURNING id as answer
                        """
                cur.execute(query, (update_start_time, notes))
                conn.commit()
                self.update_id = cur.fetchone().answer
                self.logger.info(f"Started update {self.update_id}")

        self.qOut = mp.Queue()  # the drivers will write back to this queue
        self.procs = {}  # all the collector processes. {platformID : {collecType : Collector(process, qIn)}}

        # telegram collector profiles
        # self.config['TG'] = itertools.cycle([self.config['TG']])
        self.input_dir = tempfile.mkdtemp()  # input files are downloaded here
        # additional tasks are created in files stored here
        self.overflow_task_dir = tempfile.mkdtemp()

        # platform-level collectors
        self.collectors = {}

        if collectors.get(lib.Platforms.TELEGRAM, False):
            self.collectors[lib.Platforms.TELEGRAM] = (TGCollector, collectors[lib.Platforms.TELEGRAM])
        if collectors.get(lib.Platforms.YOUTUBE, False):
            self.collectors[lib.Platforms.YOUTUBE] = (YTCollector, collectors[lib.Platforms.YOUTUBE])
        # if collectors.get(lib.Platforms.TWITTER, False):
        #    self.collectors[lib.Platforms.TWITTER] = (TWCollector, collectors[lib.Platforms.TWITTER])
        if collectors.get(lib.Platforms.WHATSAPP, False):
            self.collectors[lib.Platforms.WHATSAPP] = (WACollector, collectors[lib.Platforms.WHATSAPP])
        if collectors.get(lib.Platforms.REDDIT, False):
            self.collectors[lib.Platforms.REDDIT] = (RDCollector, collectors[lib.Platforms.REDDIT])

    def run(self, infilepaths=None, file_names=None, sheet_name_pattern=None,
            start_date=None, end_date=None,
            check_blocked=False,
            ):
        """
        Run all the collection tasks listed in the files in self.input_dir
        """

        if sheet_name_pattern is None:
            sheet_name_pattern = '.*'

        drive_files = []
        if file_names:
            self.get_files(file_names = file_names,
                           sheet_name_pattern = sheet_name_pattern,
                           )
            drive_files = sorted(glob.glob(os.path.join(self.input_dir, '*.csv')))

        if infilepaths is None:
            infilepaths = []

        new_task_files = []
        tasks = {e.value: e for e in lib.CollecTypes}

        seen_platforms = set()
        row_count = 0
        for infilepath in itertools.chain(drive_files, infilepaths, new_task_files):

            fname = os.path.basename(infilepath)
            # assume filename template is PROJECT_[PCR]_IDGAF.csv
            internal_project, pcr, idgaf = fname.split("_", 2)
            internal_project = internal_project.lower()
            task = tasks[pcr]

            if task == lib.CollecTypes.channels:  # add a pre _L task
                # cache the queue and the process manager
                old_qOut, self.qOut = self.qOut, mp.Queue()
                old_procs, self.procs = self.procs, {}
                old_overflow_task_dir, self.overflow_task_dir = self.overflow_task_dir, tempfile.mkdtemp()
                old_input_dir, self.input_dir = self.input_dir, tempfile.mkdtemp()

                # create temp _L file
                tfile = os.path.join(self.overflow_task_dir,
                                     f"{internal_project}_L_{idgaf}.csv",
                                     )

                shutil.copy2(infilepath, tfile)  # copy over the _c file as an _L file
                self.run(infilepaths=[tfile], start_date=start_date, end_date=end_date)  # run _L scraper for the same update ID

                # restore from cache
                self.qOut = old_qOut
                self.procs = old_procs
                self.overflow_task_dir = old_overflow_task_dir
                self.input_dir = old_input_dir

            if '--' in fname:
                analyst = fname.split("--", 1)[0].rsplit("_", 1)[-1].strip()
            elif internal_project.lower() == 'epic':
                analyst = 'V'
            elif internal_project.lower() == 'atticus':
                analyst = 'S'
            else:
                analyst = 'S'

            if analyst == "B":
                continue

            for plat in self.collectors:
                self.logger.info(f'DEBUG | checking plat {plat}')
                if plat in lib.SPONTANEOUS_PLATFORMS:  # these don't use the input queue,
                    self.logger.info(f'DEBUG | {plat} is spontaneous')
                    # and run an _a scrape from some external resource
                    qIn = mp.Queue()
                    analyst = None  # glue param
                    conf = {plat: self.config.get(plat)}
                    conf[plat].update({"AWS": self.config.get("AWS")})
                    conf[plat].update({k: v
                                       for k,v in self.config['projects'][internal_project].items()  # noqa E231
                                       if k not in lib.Platforms.__members__
                                       })  # add non-platform configs (so, for example translation configs)

                    p = mp.Process(target = driver,
                                   args = (self.update_id,
                                           plat,
                                           self.collectors,
                                           lib.CollecTypes.all,
                                           conf,
                                           analyst,
                                           self.config.get('database'),
                                           qIn,
                                           self.qOut,
                                           ),
                                   )
                    p.start()

                    p = Collector(p, qIn)
                    self.procs.setdefault(plat, {})[task] = p

            # remove the spontaneous platforms because we just handled them
            # this will also cause WhatsApp (or other spontaneous platform) links to be ignored in the input
            self.collectors = {k:v for k,v in self.collectors.items() if k not in lib.SPONTANEOUS_PLATFORMS}  # noqa: E231

            last_link = None
            with open(infilepath, encoding='utf-8') as infile:

                rows = csv.DictReader(infile)
                for row in rows:
                    # pull the post/channel link
                    if task in (lib.CollecTypes.retrospective, lib.CollecTypes.comments):

                        link = row['url'] = row.get('url', row.get('post_url'))

                        if not link or not link.strip():
                            continue  # skip rows with empty post_urls
                        if link == last_link:
                            continue  # for multiple sequential entries
                        last_link = link

                        if start_date or end_date:
                            date_str = row.get('Date')

                            if date_str:
                                date = dt.datetime.strptime(date_str, '%d-%m-%Y')

                                if start_date:
                                    if date < dt.datetime.strptime(start_date, "%Y-%m-%d"):
                                        continue
                                if end_date:
                                    if date > dt.datetime.strptime(end_date, "%Y-%m-%d"):
                                        continue

                    elif task in (lib.CollecTypes.channels, lib.CollecTypes.posts, lib.CollecTypes.last_post):
                        if row.get('Current Status') == 'Blocked / Deleted' and not check_blocked:
                            continue
                        link = row['url'] = row.get('channel_url', row.get('url'))

                    # / pull the post/channel link
                    if link is None or not link.strip():
                        continue

                    plat = lib.detectPlatform(link)
                    self.logger.debug(f'DEBUG: detected plat: {plat}')
                    if plat not in self.collectors:
                        self.logger.debug(f"DEBUG | {plat} not in self.collectors")
                        if plat not in seen_platforms:
                            seen_platforms.add(plat)
                            self.logger.warning(f"{plat} not in {self.collectors.keys()}")
                        continue

                    conf = self.config['projects'].get(internal_project, {})
                    conf = conf.get(plat)
                    if conf is None:
                        continue

                    conf.update({"AWS": self.config.get("AWS")})
                    plat_proc = f"{plat} | {analyst}"

                    if task not in self.procs.setdefault(plat_proc, {}):  # set up the collector process

                        config = conf
                        qIn = mp.Queue()

                        if plat == lib.Platforms.TELEGRAM:
                            config = dict(db=self.config['database'])
                        config[plat] = conf

                        config[plat].update({k: v
                                             for k,v in self.config['projects'][internal_project].items()  # noqa E231
                                             if k not in lib.Platforms.__members__
                                             })  # add non-platform configs (so, for example translation configs)  noqa E124

                        self.logger.debug(f"DEBUG | creating new process for plat {plat}")
                        p = mp.Process(target = driver,
                                       args = (self.update_id,
                                               plat,
                                               self.collectors,
                                               task,
                                               config,
                                               analyst,
                                               self.config.get('database'),
                                               qIn,
                                               self.qOut,
                                               ),
                                       )
                        self.logger.debug(f"DEBUG | starting process for plat {plat} started")
                        p.start()
                        self.logger.debug(f"DEBUG | process started for plat {plat} started")

                        p = Collector(p, qIn)
                        self.procs[plat_proc][task] = p

                    row['internal_project'] = internal_project
                    row['Start Date'] = start_date
                    row['End Date'] = end_date
                    self.procs[plat_proc][task].qIn.put(row)
                    row_count += 1

                    if task == lib.CollecTypes.channels:
                        if not row.get('Get Posts', '').strip():  # the field is empty
                            continue

                        # add a 'p' mode task
                        tfile = os.path.join(self.overflow_task_dir,
                                             os.path.basename(infilepath),
                                             f"{internal_project}_p_{idgaf}.csv",
                                             )

                        # new task file was created
                        if self.create_new_task(row, tfile):
                            new_task_files.append(tfile)

        self.logger.info(f"I had {len(self.procs)} Analysts. They were {self.procs.keys()}")
        self.logger.info(f"They processed {row_count} rows")

        if len(self.procs) == 0:  # 
            self.logger.critical("No processable data was found")
            if Hub.current.client is not None:
                Hub.current.client.flush()
            sys.exit(1)

        for fpath in drive_files:
            # only delete files that are downloaded from drive
            os.remove(fpath)

        # signal end of inputs to all procs
        for p in itertools.chain.from_iterable(d.values() for d in self.procs.values()):
            p.qIn.put(None)

        # wait for procs to finish
        for _ in itertools.chain.from_iterable(d.values() for d in self.procs.values()):
            self.qOut.get()

        # close all the queues
        for p in itertools.chain.from_iterable(d.values() for d in self.procs.values()):
            p.qIn.close()
        self.qOut.close()

        # kill procs
        for cproc in itertools.chain.from_iterable(d.values() for d in self.procs.values()):
            cproc.proc.terminate()

        shutil.rmtree(self.overflow_task_dir)  # delete the temp files
        shutil.rmtree(self.input_dir)  # delete the downloaded files

        update_end_time = dt.datetime.now()
        config = self.config['database']
        with pg.connect(host=config['host'], database=config['db_name'], user=config['user'], password=config['pass']) as conn:
            conn.set_session(autocommit=True)
            with conn.cursor(cursor_factory=pgex.NamedTupleCursor) as cur:
                query = """
                        UPDATE updates.updates
                        SET end_time = %(end_time)s
                        where id = %(id)s
                        """
                cur.execute(query,
                            dict(end_time = update_end_time.strftime("%Y-%m-%d %H:%M:%S"),
                                 id = self.update_id,
                                 ),
                            )

        return self.update_id, pcr

    def create_new_task(self, row, fpath):
        """
        Create an input file to be ingested into the master collector.
        :param row: the row from the original input csv, that should be written to the output file
        :param fpath: the filepath into which this task should be added
        :return: bool. Was a new file created?
        """

        made_new_file = False

        if not os.path.exists(fpath):
            made_new_file = True
            with open(fpath, 'w') as outfile:
                outfile = csv.DictWriter(outfile, fieldnames=row.keys())
                outfile.writeheader()

        with open(fpath, 'a') as outfile:
            outfile = csv.DictWriter(outfile, fieldnames=row.keys())
            outfile.writerow(row)

        return made_new_file

    def get_files(self, file_names=None, sheet_name_pattern='.*'):
        """
        Download all files from the shared gDrive that end in _p/_c/_r/_m
        """

        if file_names is None:
            file_names = lib.HermionesBeadedHandbag()

        D = DriveService('TEST')
        files = D.search_files('sharedWithMe and mimeType contains "spreadsheet"')

        whitelist = set(string.ascii_letters + string.digits + ' ')

        task_codes = set('pcrm')
        for file in files:
            if file['Name'] not in file_names:
                continue
            outfilename = file['Name']
            pieces = outfilename.split("_")
            if len(pieces) < 2:  # not one of our files. Move onto the next one
                continue

            task_code = pieces[1]
            if task_code not in task_codes:
                continue
            for char in outfilename:
                if char not in whitelist:
                    outfilename = outfilename.replace(char, "_")
            outfilename = f"{outfilename}.csv"

            D.download_file(file['Id'], outfilename, destination_path=self.input_dir, sheet_name_pattern=sheet_name_pattern)

    def read_config(self, infilepath):
        '''
        Read the config filepath and populate the internal config
        :param infilepath: the filepath to the master configfile
        :return: dict
        '''

        with open(infilepath) as infile:
            answer = yaml.load(infile.read(), Loader=yaml.CLoader)

        platform_codes = dict(lib.Platforms.__members__)
        for project, pconfig in answer['projects'].items():
            answer['projects'][project] = {platform_codes.get(k, k): v for k,v in pconfig.items()}  # noqa E231

        return answer


def driver(update_id, platform, collectors, task, conf, analyst, db_conf, qIn, qOut):
    '''
    This is the primary multiprocessing slave function
    :param platform: this is the platform code, used to determine the type of collector we're using
    :param analyst: this is the analyst who will analyze this platform.
                    `conf` should have an entry for this analyst.
                    If such an entry does not exist, use the global settings in conf, moving forward
    :param collectors: MasterCollector.collectors.
    :param task: p/c/r task code
    :param conf: telegram configurations to be used to create a new telegram client as required
    :param qIn: for multprocess IPC
    :param qOut: for multprocess IPC
    '''

    try:
        coll = collectors[platform][0](type=task, cli=collectors[platform][1])

        platform_conf = conf[platform]
        updates = {platform: platform_conf.get(analyst, platform_conf),
                   "AWS": conf.get("AWS"),
                   }
        conf.update(updates)
        updates = {k:v for k,v in platform_conf.items() if k not in lib.Platforms.__members__}  # noqa E231

        # this is a separate process, so it can have it's own async loop
        with pg.connect(host = db_conf['host'],
                        database = db_conf['db_name'],
                        user = db_conf['user'],
                        password = db_conf['pass']) as conn:

            conn.set_session(autocommit=True)
            with conn.cursor(cursor_factory=pgex.NamedTupleCursor) as cur:

                conf.update(dict(cursor = cur,
                                 update_id = update_id,
                                 ),
                            )

                conf['cursor'] = cur
                asyncio.run(coll.run_service(conf, qIn, qOut))

    except Exception as e:
        logging.getLogger(platform.value).critical(e)
        logging.getLogger(platform.value).critical(traceback.format_exc())
        Hub.current.client.flush()  # to avoid the subprocess dying before the log is sent to sentry
        qOut.put(platform.value)  # send back death so that the process doesn't hang


def main(tgConfigPath, collectors, infilepaths=None):
    '''
    Run all the collectors. Currently, this will run all Telegram collectors, but none for any other platforms

    :param infilepaths: each of these is a csv input with all the collection requirements
    :param configPath: the config file with API IDs and Hashes, as well as phone numbers for each telegram account
    '''

    mc = MasterCollector(tgConfigPath, collectors)
    mc.run(infilepaths)
