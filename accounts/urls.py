from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    BasicInfoView,
    UnivInfoView,
    TargetInfo01View,
    SignupView,
    CreateHobbyView,
    WelcomeView,
    ProfileView,
    MyProfileView,
    SeeRecruitView,
    BasicInfoEditView,
    UnivInfoEditView,
    ProfileTextEditView,
)

app_name = "accounts"
urlpatterns = [
    path("", WelcomeView.as_view(), name="welcome"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("basicInfo/", BasicInfoView.as_view(), name="basicInfo"),
    path("univInfo/", UnivInfoView.as_view(), name="univInfo"),
    path("targetInfo01/", TargetInfo01View.as_view(), name="targetInfo01"),
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
    path("seeRecruit/", SeeRecruitView.as_view(), name="seeRecruit"),
    path(
        "basicInfoEdit/<int:profile_id>/",
        BasicInfoEditView.as_view(),
        name="basicInfoEdit",
    ),
    path(
        "univInfoEdit/<int:profile_id>/",
        UnivInfoEditView.as_view(),
        name="univInfoEdit",
    ),
    path(
        "profileTextEdit/<int:profile_id>/",
        ProfileTextEditView.as_view(),
        name="profileTextEdit",
    ),
]
