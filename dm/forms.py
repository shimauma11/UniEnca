from django import forms
from .models import Room, Message


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("body",)


class RoomEditForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = (
            "name",
            "max_num",
        )
