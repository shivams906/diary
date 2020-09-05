from django.shortcuts import render, redirect
from entries.forms import EntryForm
from entries.models import Entry


def home(request):
    entries = Entry.objects.all()
    return render(request, "entries/home.html", {"entries": entries})


def add(request):
    form = EntryForm()
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("entries:home")
    return render(request, "entries/add.html", {"form": form})
