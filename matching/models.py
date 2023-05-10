from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Lesson
from accounts.models_sub import Target, Second_target
from .models_sub import Gender, Grade
from django.contrib.auth import get_user_model

from dm.models import Room

# Create your models here.

User = get_user_model()


AGE_CHOICES = [
    ("upper", "自分よりも年上"),
    ("same", "自分と同い年"),
    ("lower", "自分よりも年下"),
    ("whatever", "こだわりなし"),
]

# Favorは一時的な情報のため、userとは結びつけない


class Favor(models.Model):
    user = models.ForeignKey(
        User, related_name="favors", on_delete=models.CASCADE
    )
    gender = models.IntegerField(choices=Gender.choices, null=True, blank=True)
    grade = models.IntegerField(choices=Grade.choices, null=True, blank=True)
    age = models.CharField(
        choices=AGE_CHOICES, null=True, blank=True, max_length=8
    )
    target = models.IntegerField(choices=Target.choices, null=True, blank=True)
    second_target = models.IntegerField(
        choices=Second_target.choices, null=True, blank=True
    )
    num_of_people = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(400),
        ],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Favor{self.pk} by {self.user}"


class Search(models.Model):
    user = models.ForeignKey(
        User, related_name="searches", on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson, related_name="searches", on_delete=models.CASCADE, unique=False
    )
    favor = models.ForeignKey(
        Favor, related_name="searches", on_delete=models.PROTECT
    )
    room = models.ForeignKey(
        Room,
        related_name="searches",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f"{self.lesson} searched by {self.user}"
