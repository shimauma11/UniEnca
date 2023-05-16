from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    members = models.ManyToManyField(User, related_name="rooms")
    max_num = models.IntegerField(null=False, blank=False)
    can_join = models.BooleanField(default=True)
    introduction = models.TextField(max_length=400, null=True, blank=True)


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    time = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False,
    )
    body = models.TextField(
        max_length=400,
        null=False,
        blank=False,
    )
    room = models.ForeignKey(
        Room,
        related_name="messages",
        on_delete=models.CASCADE,
    )
