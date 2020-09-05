from django.test import TestCase
from entries.forms import EntryForm
from entries.models import Entry


class EntryFormTest(TestCase):
    def test_can_create_an_entry(self):
        form = EntryForm({"text": 10 * "text"})
        if form.is_valid():
            form.save()
        self.assertEqual(Entry.objects.count(), 1)