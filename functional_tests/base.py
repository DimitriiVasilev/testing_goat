from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import os


MAX_TIME = 3


def wait(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_TIME:
                    raise
                time.sleep(0.5)

    return wrapper


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

    @wait
    def wait_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, fn):
        return fn()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)
