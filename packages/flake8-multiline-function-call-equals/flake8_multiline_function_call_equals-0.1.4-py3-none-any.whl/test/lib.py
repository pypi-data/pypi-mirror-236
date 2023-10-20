import builtins
import collections
import enum
import functools
import json
import logging
import os

from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from urllib.parse import urlparse

import requests
import psycopg2 as pg
import psycopg2.extras as pgex
import pytz
import wave
import yaml

from google.cloud import speech
from googleapiclient.discovery import build
from pydub import AudioSegment
from url_normalize import url_normalize


logging.basicConfig(filename='logs/log')
logger = logging.getLogger('lib')
logger.addHandler(RotatingFileHandler('logs/log', maxBytes=10**6, backupCount=5))
logger.setLevel(logging.DEBUG)


@enum.unique
class CollecTypes(enum.Enum):
    ''' Collection methods used by all scrapers '''
    posts = 'p'
    channels = 'c'
    retrospective = 'r'
    comments = 'm'  # not compatible with all scrapers
    last_post = 'L'  # not compatible with all scrapers
    all = 'a'  # meant for device emulation scrapers


@enum.unique
class QBIT_ERROR_CODES(enum.Enum):
    '''What do the different error codes mean?'''

    GENERIC_MISSING_DATA = 'data is missing from response'
    GENERIC_URL_CHANGE = "the page's URL has changed (URL drift)"
    GENERIC_MISSING_DATA_AND_URL_CHANGE = "data is missing from response and the page's URL has changed (URL drift)"
    GENERIC_NULL_CHANNEL = "In Telegram: Unable to get the channel entity\nIn YOUTUBE: Unable to parse channel ID from URL"
    GENERIC_UNABLE_TO_FIND_CHANNEL = "Unable to find the channel based on channel_url, possibly because it's been taken down"
    GENERIC_UNABLE_TO_FIND_POST = "Unable to find post based on post_url"
    GENERIC_RATE_LIMIT_REACHED = "This API based scraper has reached the rate limit"

    TELEGRAM_JOIN_CODE = "We are currently unable to work with Telegram join codes"
    TELEGRAM_UNJOINED_PRIVATE_CHANNEL = "The puppet account has not joined this private channel, which is therefore unscrapable"

    GOOGLE_HTTP_ERROR = "Generic Google API HTTP Error. Probably malformed URL"

    YOUTUBE_VIDEOS_NOT_FOUND = "Videos were queryable for this channel. We got a null videos response, not an empty videos list"
    YOUTUBE_COMMENTS_NOT_FOUND = "Unable to query comments for this video"

    TWITTER_API_UNABLE_TO_FIND_POST = "SNScrape was unable to find tweet by URL"
    TWITTER_API_UNABLE_TO_FIND_CHANNEL = "SNScrape was unable to find the channel"


def get_platform_ids(config_filepath):
    with open(config_filepath) as infile:
        config = yaml.load(infile.read(), Loader=yaml.CLoader)
    db_conf = config['database']
    with pg.connect(host=db_conf['host'], database=db_conf['db_name'], user=db_conf['user'], password=db_conf['pass']) as conn:
        with conn.cursor(cursor_factory=pgex.NamedTupleCursor) as cur:
            query = "SELECT id,name FROM config.platforms"
            cur.execute(query)

            platform_id = {}
            for pid, name in cur:
                platform_id[name] = pid

            PLATFORM_ID = enum.Enum("PLATFORM_ID", platform_id)

    return PLATFORM_ID


def get_platform_codes(config_filepath):
    """
    Generate a mapping of domain URLs to platform names from the URLs listed in the database.
    The output should look something like {'telegram.org': Platforms.TELEGRAM}, but with all entries for all platforms

    :param config_filepath: The filepath to master_config.yaml
    :return: {'url': Platforms enum object}
    """

    platform_lookups = {e._value_: e._name_ for e in Platforms.__members__.values()}  # noqa F821 patched by __init__.py

    with open(config_filepath) as infile:
        config = yaml.load(infile.read(), Loader=yaml.CLoader)
    db_conf = config['database']
    with pg.connect(host = db_conf['host'], 
                    database = db_conf['db_name'], 
                    user = db_conf['user'], 
                    password = db_conf['pass']) as conn:
        with conn.cursor(cursor_factory=pgex.NamedTupleCursor) as cur:
            query = "SELECT name,urls FROM config.platforms"
            cur.execute(query)

            answer = {}
            for name, urls in cur:
                platform = Platforms.__getitem__(platform_lookups[name])  # noqa F821 patched by __init__.py
                for url in urls:
                    answer[url] = platform

    return answer


# these are platforms that don't have channel/post URLs
# Rather, they parse static assets stored elsewhere, but /when/ they perform the collection is triggered by a qBit run
# So far, this just means device emulation collectors

SPONTANEOUS_PLATFORMS = {'WA',
                         }


class HermionesBeadedHandbag(collections.abc.Container):
    def __contains__(self, e):
        return True


def s3_key_exists(s3_client, bucket, key):
    """
    Check if a given key exists in the given S3 bucket
    :param s3_client: a boto3 s3 client with which we'll test if a key exists
    :param bucket: the S3 bucket within which we'll check for the key
    :param key: the key (including the prefix and delimiters) to check
    :return:
    """
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=key)
    if response['KeyCount'] <= 0:  # the key wasn't found
        return False

    for obj in response['Contents']:  # something was found, so we need to check the keys now
        if key == obj['Key']:
            return True


def detectPlatform(url):
    ''' Use the url to determine what platform a link is from '''

    # stopgap hotfix, TODO return to this
    if 'tg://' in url:
        return 'NA'

    url = url_normalize(url)
    try:
        if urlparse(url).netloc in PLATFORM_CODES.keys():  # noqa F821 dynamically injected by MasterCollector
            return PLATFORM_CODES[urlparse(url).netloc]  # noqa F821 dynamically injected by MasterCollector

        try:
            service = detectService(f'https://{urlparse(url).netloc}')
        except Exception:
            logger.warning(f'unable to detect service for {url}')
            return 'NA'

        return PLATFORM_CODES.get(service, 'NA')  # noqa F821 dynamically injected by MasterCollector
    except requests.exceptions.InvalidURL:
        return 'NA'


@functools.lru_cache(maxsize=128)
def detectService(url):
    ''' Detect the net location / domain of the service'''
    service = urlparse(requests.get(url).url).netloc
    return PLATFORM_CODES.get(service)  # noqa F821 dynamically injected by MasterCollector


def convert_time(time, timezone=pytz.timezone("America/Toronto")):
    ''' Converts naive datetime objects to utc

    Parameters
    ----------
    time : datetime
        Naive datetime
    timezone : pytz.timezone
        'Local' timezone the selenium scraper is currently using.
        Defaults to developer local timezone, America/Toronto

    Returns
    -------
    utc_dt: datetime object
        datetime object in UTC time
    '''

    if time == 'err':
        return time

    dst = is_dst(timezone)
    local_dt = timezone.localize(time, is_dst=dst)
    utc_dt = local_dt.astimezone(pytz.utc)

    return utc_dt


def is_dst(tz):
    now = pytz.utc.localize(datetime.utcnow())
    return now.astimezone(tz).dst() != timedelta(0)


LINK_COLUMN = {CollecTypes.retrospective: 'post_url',
               CollecTypes.posts: 'channel_url',
               CollecTypes.channels: 'channel_url',
               }


def detect_language(s, client):
    '''
    Use Google Translate API to detect the source language of `s`.

    :param s: str or None. the source text whose language should be detected
    :param client: An authenticated Google translate client
    '''
    if s is None:
        s = ''
    s = s.strip()
    if not s:
        return '', 0

    try:
        r = requests.post("https://translation.googleapis.com/language/translate/v2/detect",
                          data = dict(q=s, key=client._developerKey),
                          )

        r = json.loads(r.content)
        r = r['data']['detections'][0][0]
    except Exception:
        return '', -1

    return r['language'], r['confidence']


def getattr(e, *attrs, default=None):
    for a in attrs:
        e = builtins.getattr(e, a, default)
        if e == default:
            return default

    return e


def get_translate_client(conf):
    '''
    Get a Google Translation client.
    :param conf: a dictionary that contains the API key fro Google Translate
    :return: a Google Translate client
    '''

    translate_client = build('translate', 'v2', developerKey=conf['api_key'])
    return translate_client


def transcribe(infilepath, lang_code, storage_client, bucket_name, speech_client):
    '''
    Given a path to an audio file (presumed to contain a recording of human speech), transcribe the speech into text.
    Return the transcribed text as a string.

    :param infilepath: the path to the input file to transcribe
    :param lang_code: the language of the returned text. The recorded speech does not need to be in the same language.
        For example, the audio file could contain speech in Russian and lang_code could be en-US (for US English).
        The output would then contain US English text
    :param storage_client: a Google Storage client to access Google Cloud buckets
    :param bucket_name: the bucket in the Google Cloud to which the input file will be uploaded for transcription
    :speech_client: the Google Speech client to be used for transcription
    :return str: The transcribed text in the input file
    '''

    with wave.open(infilepath, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()

    if channels > 1:
        sound = AudioSegment.from_wav(infilepath)
        sound = sound.set_channels(1)
        sound.export(infilepath, format="wav")

    storage_client.get_bucket(bucket_name).blob(os.path.basename(infilepath)).upload_from_filename(infilepath)
    gcs_uri = os.path.join('gs://', bucket_name, os.path.basename(infilepath))

    audio = speech.RecognitionAudio(uri=gcs_uri)
    speech_recognition_config = speech.RecognitionConfig(encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                                         sample_rate_hertz = frame_rate,
                                                         language_code = lang_code,
                                                         )
    response = speech_client.long_running_recognize(request = dict(audio = audio,
                                                                   config = speech_recognition_config,
                                                                   )
                                                    ).result()

    answer = [r.alternatives[0].transcript for r in response.results]
    storage_client.get_bucket(bucket_name).blob(os.path.basename(infilepath)).delete()

    return ' '.join(answer)
