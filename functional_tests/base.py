from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os


MAX_TIME = 3


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        server = os.environ.get('SERVER', cls.live_server_url)
        cls.server_url = server

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_TIME:
                    raise
                time.sleep(0.5)

    @staticmethod
    def wait_for(func):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_TIME:
                    raise
                time.sleep(0.5)
