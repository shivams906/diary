from django.urls import path
from diary import views

app_name = "diary"
urlpatterns = [
    path("", views.home, name="home"),
    path("add/", views.add, name="add"),
    path("set-timezone/", views.set_timezone, name="set-timezone"),
]
