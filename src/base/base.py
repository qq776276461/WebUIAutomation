from selenium import webdriver

from src.base.init_driver import init_browser_driver


class Base:

    def __init__(self, driver: webdriver = None):
        if driver is not None:
            self.__driver = driver
            return

        self.__driver = init_browser_driver('chrome')
        self.__driver.implicitly_wait(2)

    def url_get(self, url: str):
        self.__driver.get(url)

    def quit(self):
        self.__driver.quit()