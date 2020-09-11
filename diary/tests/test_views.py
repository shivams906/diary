from django.test import TestCase
from django.urls import resolve
from django.contrib.auth import get_user_model
from diary.views import home, add
from diary.forms import EntryForm
from diary.models import Entry

User = get_user_model()


class HomePageTest(TestCase):
    def test_diary_url_resolves_to_correct_view_function(self):
        found = resolve("/diary/")
        self.assertEqual(found.func, home)

    def test_unauthenticated_users_are_shown_about_template(self):
        response = self.client.get("/diary/")
        self.assertTemplateUsed(response, "diary/about.html")

    def test_authenticated_users_are_shown_home_template(self):
        user = User.objects.create_user(username="jacob", password="top_secret")
        self.client.force_login(user)
        response = self.client.get("/diary/")
        self.assertTemplateUsed(response, "diary/home.html")

    def test_home_view_shows_diary(self):
        user = User.objects.create_user(username="jacob", password="top_secret")
        self.client.force_login(user)
        self.client.post("/diary/add/", {"text": 10 * "text"})
        response = self.client.get("/diary/")
        data = response.content.decode("utf-8")
        self.assertIn(10 * "text", data)


class AddPageTest(TestCase):
    def test_add_url_resolves_to_correct_view_function(self):
        found = resolve("/diary/add/")
        self.assertEqual(found.func, add)

    def test_add_view_uses_correct_template(self):
        response = self.client.get("/diary/add/")
        self.assertTemplateUsed(response, "diary/add.html")

    def test_add_view_uses_correct_form(self):
        response = self.client.get("/diary/add/")
        self.assertIsInstance(response.context["form"], EntryForm)

    def test_POST_creates_an_entry(self):
        self.client.post("/diary/add/", {"text": 10 * "text"})
        self.assertEqual(Entry.objects.count(), 1)

    def test_POST_does_not_create_blank_diary(self):
        self.client.post("/diary/add/", {"text": ""})
        self.assertEqual(Entry.objects.count(), 0)

    def test_valid_POST_redirects_to_home_page(self):
        response = self.client.post("/diary/add/", {"text": 10 * "text"})
        self.assertRedirects(response, "/diary/")
