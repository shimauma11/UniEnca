from django.db import models


class Gender(models.IntegerChoices):
    male = 0, "男性"
    female = 1, "女性"
    others = 2, "その他"


class Grade(models.IntegerChoices):
    grade_1 = 1, "1年生"
    grade_2 = 2, "2年生"
    grade_3 = 3, "3年生"
    grade_4 = 4, "4年生"


class Target(models.IntegerChoices):
    for_encounter = 0, "新しい出会いのため"
    for_credit = 1, "単位取得のため"


class Second_target(models.IntegerChoices):
    like_you = 0, "あなたと似ている人"
    not_like_you = 1, "あなたと似ていない人"


class Day_of_week(models.IntegerChoices):
    sun = 0, "日"
    mon = 1, "月"
    tue = 2, "火"
    wed = 3, "水"
    thu = 4, "木"
    fri = 5, "金"
    sat = 6, "土"


class Time(models.IntegerChoices):
    time1 = 1, "1限"
    time2 = 2, "2限"
    time3 = 3, "3限"
    time4 = 4, "4限"
    time5 = 5, "5限"
    time6 = 6, "6限"
    time7 = 7, "7限"


class Hobby_kind(models.IntegerChoices):
    indoor = 0, "インドア"
    outdoor = 1, "アウトドア"
    another = 2, "その他" 