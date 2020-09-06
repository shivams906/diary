from django.test import TestCase
from entries.models import Entry


class EntryTest(TestCase):
    def test_can_create_an_entry(self):
        entry = Entry.objects.create(text=10 * "text")
        self.assertEqual(Entry.objects.count(), 1)

    def test_can_test_change_modified_date(self):
        entry = Entry.objects.create(text=10 * "text")
        modified_date = entry.modified
        entry.text = "text"
        entry.save()
        self.assertLess(modified_date, entry.modified)

    def test_saves_entries_ordered_ny_date(self):
        entry1 = Entry.objects.create(text=10 * "text")
        entry2 = Entry.objects.create(text=10 * "text")
        self.assertEqual(Entry.objects.first(), entry2)