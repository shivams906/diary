from django.test import TestCase
from django.urls import resolve
from entries.views import home, add


class HomePageTest(TestCase):
    def test_entries_url_resolves_to_correct_view_function(self):
        found = resolve("/entries/")
        self.assertEqual(found.func, home)

    def test_home_view_uses_correct_template(self):
        response = self.client.get("/entries/")
        self.assertTemplateUsed(response, "entries/home.html")


class AddPageTest(TestCase):
    def test_add_url_resolves_to_correct_view_function(self):
        found = resolve("/entries/add/")
        self.assertEqual(found.func, add)

    def test_add_view_uses_correct_template(self):
        response = self.client.get("/entries/add/")
        self.assertTemplateUsed(response, "entries/add.html")