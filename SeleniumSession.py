from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Page.ProductListPage import ProductListPage


def openPage(cls, *args):
    page = cls(*args)
    page.open()

    return page


class SeleniumSession:
    def __init__(self, config):
        self.driver = None
        self.config = config

    def initializeWebDriver(self):
        options = Options()
        options.add_argument(f"user-data-dir={self.config.get('chrome_user_data_dir')}")
        options.add_argument('profile-directory=Profile 3')
        options.add_argument("--remote-debugging-port=9222")
        options.headless = False

        self.driver = webdriver.Chrome(options=options)

    def quit(self):
        self.driver.close()

    def openPage(self, pageCls):
        openPage(pageCls, self.driver)

        return ProductListPage(self.driver, self.config)

    def getCookies(self):
        return self.driver.get_cookies()

    def getDriver(self):
        return self.driver
