from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .models_sub import (
    Gender,
    Grade,
    Target,
    Second_target,
    Day_of_week,
    Time,
    Hobby_kind,
)


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)
    followings = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True
    )

    def __str__(self):
        return f"{self.username}"


class Hobby(models.Model):
    hobby_name = models.CharField(max_length=30, null=True, blank=True)
    hobby_kind = models.IntegerField(
        choices=Hobby_kind.choices, null=True, blank=True
    )

    def __str__(self):
        return f"{self.hobby_name}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=20, null=True, blank=True)
    gender = models.IntegerField(choices=Gender.choices, null=True, blank=True)
    grade = models.IntegerField(choices=Grade.choices, null=True, blank=True)
    age = models.IntegerField(
        validators=[
            MinValueValidator(18),
            MaxValueValidator(120),
        ],
        null=True,
        blank=True,
    )
    target = models.IntegerField(choices=Target.choices, null=True, blank=True)
    second_target = models.IntegerField(
        choices=Second_target.choices, null=True, blank=True
    )

    univ_name = models.CharField("大学名", max_length=20, null=True, blank=True)
    faculty = models.CharField("学部名", max_length=20, null=True, blank=True)
    major = models.CharField("学科名", max_length=20, null=True, blank=True)
    campus = models.CharField("キャンパス名", max_length=20, null=True, blank=True)

    profile_text = models.TextField(max_length=300, null=True, blank=True)

    hobby = models.ManyToManyField(Hobby, related_name="profiles", blank=True)

    def __str__(self):
        return f"{self.nickname}'s profile"


class Lesson(models.Model):
    students = models.ManyToManyField(User, related_name="lessons")
    lesson_name = models.CharField("科目名", max_length=30)
    day_of_week = models.IntegerField(
        choices=Day_of_week.choices, null=True, blank=True
    )
    time = models.IntegerField(choices=Time.choices, null=True, blank=True)
    univ_name = models.CharField("大学名", max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.lesson_name}"
