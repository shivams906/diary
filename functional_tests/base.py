from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
import time
import random

User = get_user_model()

MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary("/usr/lib/firefox/firefox")
        )

    def tearDown(self):
        self.browser.quit()

    def login_user(self, username, password):
        User.objects.create_user(username=username, password=password)
        self.browser.get(f"{self.live_server_url}/accounts/login/")
        wait_for(lambda: self.assertIn("Login", self.browser.title))
        wait_for(lambda: self.browser.find_element_by_id("id_username")).send_keys(
            username
        )
        wait_for(lambda: self.browser.find_element_by_id("id_password")).send_keys(
            password
        )
        wait_for(lambda: self.browser.find_element_by_id("id_login")).click()


def wait_for(function):
    start_time = time.time()
    while True:
        try:
            return function()
        except WebDriverException as exception:
            if time.time() - start_time > MAX_WAIT:
                raise exception
            time.sleep(0.5)