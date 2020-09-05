from django.test import TestCase
from django.urls import resolve
from entries.views import home, add
from entries.forms import EntryForm
from entries.models import Entry


class HomePageTest(TestCase):
    def test_entries_url_resolves_to_correct_view_function(self):
        found = resolve("/entries/")
        self.assertEqual(found.func, home)

    def test_home_view_uses_correct_template(self):
        response = self.client.get("/entries/")
        self.assertTemplateUsed(response, "entries/home.html")

    def test_home_view_shows_entries(self):
        self.client.post("/entries/add/", {"text": 10 * "text"})
        response = self.client.get("/entries/")
        data = response.content.decode("utf-8")
        self.assertIn(10 * "text", data)


class AddPageTest(TestCase):
    def test_add_url_resolves_to_correct_view_function(self):
        found = resolve("/entries/add/")
        self.assertEqual(found.func, add)

    def test_add_view_uses_correct_template(self):
        response = self.client.get("/entries/add/")
        self.assertTemplateUsed(response, "entries/add.html")

    def test_add_view_uses_correct_form(self):
        response = self.client.get("/entries/add/")
        self.assertIsInstance(response.context["form"], EntryForm)

    def test_POST_creates_an_entry(self):
        self.client.post("/entries/add/", {"text": 10 * "text"})
        self.assertEqual(Entry.objects.count(), 1)

    def test_POST_does_not_create_blank_entries(self):
        self.client.post("/entries/add/", {"text": ""})
        self.assertEqual(Entry.objects.count(), 0)

    def test_valid_POST_redirects_to_home_page(self):
        response = self.client.post("/entries/add/", {"text": 10 * "text"})
        self.assertRedirects(response, "/entries/")
