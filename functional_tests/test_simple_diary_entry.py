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
        self.browser.get(f"{self.live_server_url}/entries/")

        # She sees 'Diary' in the title
        self.assertIn("Diary", self.browser.title)

        # She sees a link to create a new entry
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()

        # She sees a text box for entering the entry
        input_box = wait_for(lambda: self.browser.find_element_by_id("id_text"))

        # She enters an entry and clicks the add button
        input_box.send_keys(10 * f'{10 * "text"}\n')
        wait_for(lambda: self.browser.find_element_by_tag_name("button")).click()

        # She is taken back to home page with her entry shown on top
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/entries/"
            )
        )

        entries = wait_for(lambda: self.browser.find_elements_by_id("id-entry"))
        self.assertIn("text", entries[0].text)

        # She enters another entry and it appears on top of it
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()
        input_box = wait_for(lambda: self.browser.find_element_by_id("id_text"))
        input_box.send_keys(10 * f'{10 * "text2"}\n')
        wait_for(lambda: self.browser.find_element_by_tag_name("button")).click()
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/entries/"
            )
        )
        entries = wait_for(lambda: self.browser.find_elements_by_id("id-entry"))
        self.assertIn("text2", entries[0].text)
        self.assertIn("text", entries[1].text)


def wait_for(function):
    start_time = time.time()
    while True:
        try:
            return function()
        except WebDriverException as exception:
            if time.time() - start_time > MAX_WAIT:
                raise exception
            time.sleep(0.5)
