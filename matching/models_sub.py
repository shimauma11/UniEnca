from django.db import models


class Gender(models.IntegerChoices):
    male = 0, "男性"
    female = 1, "女性"
    others = 2, "その他"
    whatever = 3, "こだわりなし"


class Grade(models.IntegerChoices):
    grade_1 = 1, "1年生"
    grade_2 = 2, "2年生"
    grade_3 = 3, "3年生"
    grade_4 = 4, "4年生"
    whatever = 5, "こだわりなし"
