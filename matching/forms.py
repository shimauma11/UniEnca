from django import forms
from accounts.models import Lesson


class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            "lesson_name",
            "day_of_week",
            "time",
        )
