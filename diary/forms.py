from diary.models import Entry
from django import forms


class EntryForm(forms.ModelForm):
    def save(self, owner):
        Entry.objects.create(text=self.cleaned_data["text"], owner=owner)

    class Meta:
        model = Entry
        fields = ("text",)
