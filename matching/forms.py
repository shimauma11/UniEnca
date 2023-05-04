from django import forms
from accounts.models import Lesson
from .models import Favor


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            "lesson_name",
            "day_of_week",
            "time",
        )


class CreateFavorForm(forms.ModelForm):
    class Meta:
        model = Favor
        fields = (
            "gender",
            "grade",
            "age",
            "num_of_people",
        )
