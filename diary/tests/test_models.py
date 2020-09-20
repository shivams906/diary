from django.test import TestCase
from django.contrib.auth import get_user_model
from diary.models import Entry

User = get_user_model()


class EntryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="password123")

    def test_can_create_an_entry(self):
        Entry.objects.create(text=10 * "text", owner=self.user)
        self.assertEqual(Entry.objects.count(), 1)

    def test_can_test_change_modified_date(self):
        entry = Entry.objects.create(text=10 * "text", owner=self.user)
        modified_date = entry.modified
        entry.text = "text"
        entry.save()
        self.assertLess(modified_date, entry.modified)

    def test_saves_diary_ordered_ny_date(self):
        entry1 = Entry.objects.create(text=10 * "text", owner=self.user)
        entry2 = Entry.objects.create(text=10 * "text", owner=self.user)
        self.assertEqual(Entry.objects.first(), entry2)

    def test_saves_owner_with_entry(self):
        entry = Entry.objects.create(text="entry", owner=self.user)
        self.assertIn(entry, self.user.entry_set.all())

    def test_shows_only_the_user_entries(self):
        user1 = User.objects.create_user(username="user1", password="password123")
        user2 = User.objects.create_user(username="user2", password="password123")
        entry1 = Entry.objects.create(text="entry", owner=user1)
        entry2 = Entry.objects.create(text="entry", owner=user2)
        self.assertIn(entry1, user1.entry_set.all())
        self.assertNotIn(entry2, user1.entry_set.all())