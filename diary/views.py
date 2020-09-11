from django.shortcuts import render, redirect
from diary.forms import EntryForm
from diary.models import Entry


def home(request):
    if request.user.is_authenticated:
        entries = Entry.objects.all()
        return render(request, "diary/home.html", {"entries": entries})
    else:
        return render(request, "diary/about.html")


def add(request):
    form = EntryForm()
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("diary:home")
    return render(request, "diary/add.html", {"form": form})
