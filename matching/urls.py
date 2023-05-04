from django.urls import path
from .views import (
    HomeView,
    CreateLessonView,
    CreateFavorView,
    CreateSearchView,
    SearchView,
    DeleteSearchView,
)

app_name = "matching"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("createLesson/", CreateLessonView.as_view(), name="createLesson"),
    path(
        "createFavor/<int:lesson_id>/",
        CreateFavorView.as_view(),
        name="createFavor",
    ),
    path(
        "createSearch/<int:lesson_id>/<int:favor_id>/",
        CreateSearchView.as_view(),
        name="createSearch",
    ),
    path("search/<int:search_id>/", SearchView.as_view(), name="search"),
    path(
        "deleteSearch/<int:pk>/",
        DeleteSearchView.as_view(),
        name="deleteSearch",
    ),
]
