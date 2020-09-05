from django.shortcuts import render


def home(request):
    return render(request, "entries/home.html")


def add(request):
    return render(request, "entries/add.html")
