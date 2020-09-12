from .base import *


class MyDiaryTest(FunctionalTest):
    def test_separate_diary_for_separate_users(self):
        User.objects.create_user(username="edith", password="top_secret")
        User.objects.create_user(username="meredith", password="top_secret")

        # Edith logs in and enters an entry
        self.login_user(username="edith", password="top_secret")
        self.browser.get(f"{self.live_server_url}/diary/")
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()
        input_box = wait_for(lambda: self.browser.find_element_by_id("id_text"))
        input_box.send_keys(10 * f'{10 * "entry1"}\n')
        wait_for(lambda: self.browser.find_element_by_tag_name("button")).click()

        # She sees te entry on the homepage
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/diary/"
            )
        )
        diary = wait_for(lambda: self.browser.find_elements_by_class_name("entry"))
        self.assertIn("entry1", diary[0].text)

        # She logs out
        wait_for(lambda: self.browser.find_element_by_link_text("Logout")).click()

        # Meredith logs in
        self.login_user(username="meredith", password="top_secret")

        # She doesn't see edith's entry
        entries = wait_for(lambda: self.browser.find_elements_by_class_name("entry"))
        self.assertFalse(any(["entry1" in entry.text for entry in entries]))

        # She enters an entry
        wait_for(lambda: self.browser.find_element_by_link_text("Add")).click()
        input_box = wait_for(lambda: self.browser.find_element_by_id("id_text"))
        input_box.send_keys(10 * f'{10 * "entry2"}\n')
        wait_for(lambda: self.browser.find_element_by_tag_name("button")).click()

        # She sees her entry
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, f"{self.live_server_url}/diary/"
            )
        )
        entries = wait_for(lambda: self.browser.find_elements_by_class_name("entry"))
        self.assertTrue(any(["entry2" in entry.text for entry in entries]))
        self.assertFalse(any(["entry1" in entry.text for entry in entries]))

        # She logs out
        wait_for(lambda: self.browser.find_element_by_link_text("Logout")).click()

        # Edith logs in again
        self.login_user(username="edith", password="top_secret")

        # She sees only her entry and not meredith's
        self.browser.get(f"{self.live_server_url}/diary/")
        entries = wait_for(lambda: self.browser.find_elements_by_class_name("entry"))
        self.assertTrue(any(["entry1" in entry.text for entry in entries]))
        self.assertFalse(any(["entry2" in entry.text for entry in entries]))