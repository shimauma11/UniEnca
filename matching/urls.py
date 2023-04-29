from django.urls import path
from .views import HomeView, CreateLessonView

app_name = "matching"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("createLesson/", CreateLessonView.as_view(), name="createLesson"),
]