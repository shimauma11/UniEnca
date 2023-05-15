from django.urls import path
from .views import (
    HomeView,
    CreateLessonView,
    CreateFavorView,
    CreateSearchView,
    SearchView,
    CreateRecruitView,
    DeleteFavorView,
)

app_name = "matching"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "createLesson/<str:path>/",
        CreateLessonView.as_view(),
        name="createLesson",
    ),
    path(
        "createFavor/<int:lesson_id>/<str:path>/",
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
        "createRecruit/<int:lesson_id>/<int:favor_id>/",
        CreateRecruitView.as_view(),
        name="createRecruit",
    ),
    path("delete/<int:pk>/", DeleteFavorView.as_view(), name="delete"),
]
