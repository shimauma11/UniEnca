from django import forms
from .models import Room, Message


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = (
            "max_num",
        )


class MessageSendForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            "body",
        )