from django.test import TestCase
from django.contrib.auth import get_user_model
from diary.forms import EntryForm
from diary.models import Entry

User = get_user_model()


class EntryFormTest(TestCase):
    def test_can_create_an_entry(self):
        user = User.objects.create_user(username="user", password="top_secret")
        form = EntryForm({"text": 10 * "text"})
        if form.is_valid():
            form.save(owner=user)
        self.assertEqual(Entry.objects.count(), 1)

    def test_saves_owner_with_entry(self):
        user = User.objects.create_user(username="user", password="top_secret")
        form = EntryForm({"text": 10 * "text"})
        if form.is_valid():
            form.save(owner=user)
        self.assertEqual(Entry.objects.first().owner, user)