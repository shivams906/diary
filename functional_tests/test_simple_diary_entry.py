from .base import *


class HomePageTest(FunctionalTest):
    def setUp(self):
        self.browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary("/usr/lib/firefox/firefox")
        )

    def tearDown(self):
        self.browser.quit()

    def test_simple_diary_entry(self):
        User.objects.create_user(username="edith", password="top_secret")
        self.login_user(username="edith", password="top_secret")

        # Edith goes to the home page
        self.browser.get(f"{self.live_server_url}/diary/")

        # She sees 'Diary' in the title
        self.assertIn("Diary", self.browser.title)

        # She sees a link to create a new entry
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()

        # She sees a text box for entering the entry
        input_box = wait_for(lambda: self.browser.find_element_by_id("id_text"))

        # She enters an entry and clicks the add button
        input_box.send_keys(10 * f'{10 * "entry1"}\n')
        wait_for(lambda: self.browser.find_element_by_tag_name("button")).click()

        # She is taken back to home page with her entry shown on top
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/diary/"
            )
        )

        diary = wait_for(lambda: self.browser.find_elements_by_class_name("entry"))
        self.assertIn("entry1", diary[0].text)

        # She enters another entry and it appears on top of it
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()
        input_box = wait_for(lambda: self.browser.find_element_by_id("id_text"))
        input_box.send_keys(10 * f'{10 * "entry2"}\n')
        wait_for(lambda: self.browser.find_element_by_tag_name("button")).click()
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/diary/"
            )
        )
        diary = wait_for(lambda: self.browser.find_elements_by_class_name("entry"))
        self.assertIn("entry2", diary[0].text)
        self.assertIn("entry1", diary[1].text)
