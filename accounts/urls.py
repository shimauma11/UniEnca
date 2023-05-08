from django.urls import path
from .views import (
    UserLoginView,
    BasicInfoView,
    UnivInfoView,
    TargetInfo01View,
    TargetInfo02View,
    SignupView,
    CreateHobbyView,
    WelcomeView,
    ProfileView,
    MyProfileView,
    SeeSearchView,
)

app_name = "accounts"
urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("basicInfo/", BasicInfoView.as_view(), name="basicInfo"),
    path("univInfo/", UnivInfoView.as_view(), name="univInfo"),
    path("targetInfo01/", TargetInfo01View.as_view(), name="targetInfo01"),
    path("targetInfo02/", TargetInfo02View.as_view(), name="targetInfo02"),
    path(
        "createHobby/",
        CreateHobbyView.as_view(),
        name="createHobby",
    ),
    path(
        "myPofile/",
        MyProfileView.as_view(),
        name="myProfile",
    ),
    path(
        "profile/<int:user_id>/<int:search_id>/",
        ProfileView.as_view(),
        name="profile",
    ),
    path("seeSearch/", SeeSearchView.as_view(), name="seeSearch"),
]
