from django.urls import path
from entries import views

app_name = "entries"
urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),
]
