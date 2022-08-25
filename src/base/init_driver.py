import os
import sys

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EService
from selenium.webdriver.firefox.service import Service as FService
from selenium.webdriver.safari.service import Service as SafariServive
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.manager import DriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.utils import get_browser_version_from_os, ChromeType, File

from src.utils.ConfigRead import CONFIG
from src.utils.HookMethod import get_url, file_name, get_driver_path
from src.utils.Log import init_log
from src.utils.PathUtil import path_join


class BrowserNotFond(Exception):

    def __init__(self, browser_name):
        self.browser_name = browser_name

    def __str__(self, *args, **kwargs):
        return f"检查到本机未安装{self.browser_name}浏览器, 请安装{self.browser_name}浏览器"


class BrowserType:
    Chrome = ChromeType.GOOGLE
    Firefox = 'firefox'
    Edge = ChromeType.MSEDGE
    Safari = 'safari'


def init_browser_driver(browser_type, driver_cache_day=365):
    GeckoDriver.get_url = get_url
    File.filename = file_name
    DriverManager._get_driver_path = get_driver_path
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOCAL'] = '1'
    os.environ['WDM_SSL_VERIFY'] = '1'
    _log = init_log()
    browser = browser_type
    browser_exists = None
    browser_list = ['chrome', 'firefox', 'edge', 'safari']
    if browser_type not in browser_list:
        raise BrowserNotFond(browser_type)
    if browser == 'chrome':
        browser = BrowserType.Chrome
    if browser != BrowserType.Safari:
        browser_exists = get_browser_version_from_os(browser)
    if (browser_type == BrowserType.Safari and sys.platform != 'darwin') or browser_exists is None:
        raise BrowserNotFond(browser_type)
    _log.info(f"当前的{browser_type}浏览器版本是: {browser_exists}, 正在准备{browser_type}浏览器的webdriver...")
    if browser_type == 'chrome':
        driver_path = ChromeDriverManager(cache_valid_range=driver_cache_day, path=path_join('lib')).install()
        _log.info(f"[{browser_type}] webdriver准备完成,存放路径: {driver_path}")
        return webdriver.Chrome(service=ChromeService(driver_path), chrome_options=__get_chrome_options())
    elif browser_type == 'firefox':
        driver_path = GeckoDriverManager(url="https://repo.huaweicloud.com/geckodriver",
                                         cache_valid_range=driver_cache_day,
                                         path=path_join('lib')).install()
        _log.info(f"[{browser_type}] webdriver准备完成,存放路径: {driver_path}")
        return webdriver.Firefox(service=FService(driver_path))
    elif browser_type == 'edge':
        driver_path = EdgeChromiumDriverManager(cache_valid_range=driver_cache_day,
                                                path=path_join('lib')).install()
        _log.info(f"[{browser_type}] webdriver准备完成,存放路径: {driver_path}")
        return webdriver.Edge(service=EService(driver_path))
    elif browser_type == 'safari':
        return webdriver.Chrome(service=SafariServive())


def __get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_config = CONFIG.chrome_config
    for key, value in chrome_config.items():
        if key == 'disable-infobars' and value:
            chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
            continue
        if key == 'pass-save' and value:
            prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
            chrome_options.add_experimental_option("prefs", prefs)
            continue
        if value:
            chrome_options.add_argument(f'{key}={value}')
    return chrome_options


if __name__ == '__main__':
    init_browser_driver('edge')
