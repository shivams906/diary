from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from diary.views import home, add
from diary.forms import EntryForm
from diary.models import Entry

User = get_user_model()


class HomePageTest(TestCase):
    def test_diary_url_resolves_to_correct_view_function(self):
        found = resolve(reverse("diary:home"))
        self.assertEqual(found.func, home)

    def test_unauthenticated_users_are_shown_about_template(self):
        response = self.client.get(reverse("diary:home"))
        self.assertTemplateUsed(response, "diary/about.html")

    def test_authenticated_users_are_shown_home_template(self):
        user = User.objects.create_user(username="user", password="password123")
        self.client.force_login(user)
        response = self.client.get(reverse("diary:home"))
        self.assertTemplateUsed(response, "diary/home.html")

    def test_home_view_shows_diary(self):
        user = User.objects.create_user(username="user", password="password123")
        self.client.force_login(user)
        self.client.post(reverse("diary:add"), {"text": 10 * "text"})
        response = self.client.get(reverse("diary:home"))
        data = response.content.decode("utf-8")
        self.assertIn(10 * "text", data)

    def test_only_current_users_entries_are_displayed(self):
        user1 = User.objects.create_user(username="user1", password="password123")
        user2 = User.objects.create_user(username="user2", password="password123")
        entry1 = Entry.objects.create(text="entry1", owner=user1)
        entry2 = Entry.objects.create(text="entry2", owner=user2)

        self.client.force_login(user1)

        response = self.client.get(reverse("diary:home"))
        entries = response.context["entries"]
        self.assertIn(entry1, entries)
        self.assertNotIn(entry2, entries)


class AddPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password123")

    def test_add_url_resolves_to_correct_view_function(self):
        self.client.force_login(self.user)
        found = resolve(reverse("diary:add"))
        self.assertEqual(found.func, add)

    def test_add_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("diary:add"))
        self.assertTemplateUsed(response, "diary/add.html")

    def test_redirects_to_login_page_for_unauthenticated_users(self):
        response = self.client.get(reverse("diary:add"))
        self.assertRedirects(response, "/accounts/login/?next=/diary/add/")

    def test_add_view_uses_correct_form(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("diary:add"))
        self.assertIsInstance(response.context["form"], EntryForm)

    def test_POST_creates_an_entry(self):
        self.client.force_login(self.user)
        self.client.post(reverse("diary:add"), {"text": 10 * "text"})
        self.assertEqual(Entry.objects.count(), 1)

    def test_POST_does_not_create_blank_diary(self):
        self.client.force_login(self.user)
        self.client.post(reverse("diary:add"), {"text": ""})
        self.assertEqual(Entry.objects.count(), 0)

    def test_valid_POST_redirects_to_home_page(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("diary:add"), {"text": 10 * "text"})
        self.assertRedirects(response, reverse("diary:home"))

    def test_current_user_is_saved_as_owner(self):
        self.client.force_login(self.user)
        self.client.post(reverse("diary:add"), {"text": 10 * "text"})
        entry = Entry.objects.first()
        self.assertEqual(entry.owner, self.user)
