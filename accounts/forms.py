from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Profile, Hobby

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = field.label


class BasicInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "nickname",
            "gender",
            "grade",
            "age",
            "profile_text",
        )

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get("age")

        if age < 18 or 120 < age:
            raise ValidationError("18歳から120歳の間で入力してください")


class UnivInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "univ_name",
            "faculty",
            "major",
            "campus",
        )


class TargetInfo01Form(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("target",)


class CreateHobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = (
            "hobby_name",
            "hobby_kind",
        )


class BasicInfoEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "nickname",
            "gender",
            "grade",
            "age",
        )


class UnivInfoEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "univ_name",
            "faculty",
            "major",
            "campus",
        )


class ProfileTextEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_text",)
