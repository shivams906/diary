from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time

MAX_WAIT = 5


class HomePageTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary("/usr/lib/firefox/firefox")
        )

    def tearDown(self):
        self.browser.quit()

    def test_simple_diary_entry(self):
        # Edith goes to the home page
        self.browser.get("http://localhost:8000/entries/")

        # She sees 'Diary' in the title
        self.assertIn("Diary", self.browser.title)

        # She sees a link to create a new entry
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()

        # She sees a text box for entering the entry
        wait_for(lambda: self.browser.find_element_by_id("id_text"))


def wait_for(function):
    start_time = time.time()
    while True:
        try:
            return function()
        except WebDriverException as exception:
            if time.time() - start_time > MAX_WAIT:
                raise exception
            time.sleep(0.5)
