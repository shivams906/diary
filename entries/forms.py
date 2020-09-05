from entries.models import Entry
from django import forms


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ("text",)
