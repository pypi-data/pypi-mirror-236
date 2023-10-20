import os
import pickle

import requests
import pytz
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common import exceptions as selException

from webdriver_manager.firefox import GeckoDriverManager

import traceback


# signal TOR for a new connection
def switchIP(collector):
    collector.logger.debug('Switching IP')
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

    collector.timezone = pytz.timezone(check_timezone(collector.browser))
    collector.logger.info(f'New timezone: {collector.timezone}')


def setup_browser(collector, proxy=False, debug=False):
    ''' Create a new browser window using Firefox and selenium webdriver and assign to the passed in collector object
        Proxy mode requires that tor is running as a service in the background
    '''

    if collector.browser:
        collector.browser.close()

    profile = webdriver.FirefoxProfile()

    options = Options()

    if not debug:
        # headless browsing
        options.headless = True

    if proxy:
        # using tor server to set up a socks proxy
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", '127.0.0.1')
        profile.set_preference("network.proxy.socks_port", 9150)
        profile.set_preference("network.proxy.socks_remote_dns", False)

    # general settings to decrease popups and notifications from social media websites
    profile.set_preference("media.autoplay.enabled", False)
    profile.set_preference("permissions.default.desktop-notification", 1)
    profile.set_preference("dom.webnotifications.enabled", 1)
    profile.set_preference("dom.push.enabled", 1)
    profile.update_preferences()

    try:
        browser = webdriver.Firefox(executable_path = GeckoDriverManager().install(),
                                    options = options,
                                    firefox_profile = profile,
                                    )
    except Exception as E:
        collector.logger.error(traceback.print_exc())
        raise E

    if os.path.exists(collector.cookie_path):
        with open(collector.cookie_path, 'rb') as infile:
            cookies = pickle.load(infile)
            for cookie in cookies:
                browser.add_cookie(cookie)

    browser.implicitly_wait(collector.delay)

    collector.browser = browser
    collector.timezone = pytz.timezone(check_timezone(browser))
    collector.logger.info(f'Browser timezone: {collector.timezone}')
    return browser


def check_timezone(browser):
    # uses whatsmyip.com and ipwhois.app to find the timezone of the current browser exit node
    # TODO error handling
    browser.get('https://ipecho.net/plain')

    try:
        ip = browser.find_element_by_tag_name('body').text
    except selException.NoSuchElementException:
        raise Exception('Could not identify IP address using ipecho')

    r = requests.get(f'http://ipwhois.app/json/{ip}')

    r_json = r.json()
    return r_json.get('timezone')


def get_timezone_offset(browser):
    """
    Fetch current IP address from IPEcho and feed that into ipwhois to get current timezone offset from UTC
    :param browser: Selenium browser instance
    :return: timezone offset
    """
    browser.get('https://ipecho.net/plain')

    try:
        ip = browser.find_element_by_tag_name('body').text
    except selException.NoSuchElementException:
        raise Exception('Could not identify IP address using ipecho')

    resp = requests.get(f'http://ipwhois.app/json/{ip}')
    return resp.json().get('timezone_gmt')
