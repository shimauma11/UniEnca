from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile, Lesson, Hobby
# Register your models here.

User = get_user_model()

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Lesson)
admin.site.register(Hobby)