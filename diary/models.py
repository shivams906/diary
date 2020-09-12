from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Entry(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created",)
