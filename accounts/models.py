from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .models_sub import Gender, Grade, Target, Second_target, Day_of_week, Time


class User(AbstractUser):
    email = models.EmailField("メールアドレス", unique=True)
    followings = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True
    )
    # ここに、reportとfavor,hobby,


class Univ(models.Model):
    univ_name = models.CharField("大学名", max_length=20)
    faculty = models.CharField("学部名", max_length=20)
    major = models.CharField("学科名", max_length=20)
    campus = models.CharField("キャンパス名", max_length=20)
    user = models.OneToOneField(User, related_name="univ", on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
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
    profile_text = models.TextField(max_length=300, null=True, blank=True)
    univ = models.ForeignKey(
        Univ,
        related_name="students",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )


class Lesson(models.Model):
    student = models.ManyToManyField(User, related_name="lessons")
    lesson_name = models.CharField("科目名", max_length=30)
    day_of_week = models.IntegerField(
        choices=Day_of_week.choices, null=True, blank=True
    )
    time = models.IntegerField(choices=Time.choices, null=True, blank=True)
    univ = models.ForeignKey(
        Univ, related_name="lessons", on_delete=models.CASCADE
    )
