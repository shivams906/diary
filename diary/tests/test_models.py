from django.test import TestCase
from django.contrib.auth import get_user_model
from diary.models import Entry

User = get_user_model()


class EntryTest(TestCase):
    def test_can_create_an_entry(self):
        user = User.objects.create_user(username="user", password="top_secret")
        entry = Entry.objects.create(text=10 * "text", owner=user)
        self.assertEqual(Entry.objects.count(), 1)

    def test_can_test_change_modified_date(self):
        user = User.objects.create_user(username="user", password="top_secret")
        entry = Entry.objects.create(text=10 * "text", owner=user)
        modified_date = entry.modified
        entry.text = "text"
        entry.save()
        self.assertLess(modified_date, entry.modified)

    def test_saves_diary_ordered_ny_date(self):
        user = User.objects.create_user(username="user", password="top_secret")
        entry1 = Entry.objects.create(text=10 * "text", owner=user)
        entry2 = Entry.objects.create(text=10 * "text", owner=user)
        self.assertEqual(Entry.objects.first(), entry2)

    def test_saves_owner_with_entry(self):
        user = User.objects.create_user(username="user", password="top_secret")
        entry = Entry.objects.create(text="entry", owner=user)
        self.assertIn(entry, user.entry_set.all())

    def test_shows_only_the_user_entries(self):
        user1 = User.objects.create_user(username="user1", password="top_secret")
        user2 = User.objects.create_user(username="user2", password="top_secret")
        entry1 = Entry.objects.create(text="entry", owner=user1)
        entry2 = Entry.objects.create(text="entry", owner=user2)
        self.assertIn(entry1, user1.entry_set.all())
        self.assertNotIn(entry2, user1.entry_set.all())