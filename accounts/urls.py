from django.urls import path
from .views import UserLoginView, BasicInfoView, UnivInfoView, TargetInfo01View, TargetInfo02View, SignupView

app_name = "accounts"
urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("basicInfo/", BasicInfoView.as_view(), name="basicInfo"),
    path("univInfo/", UnivInfoView.as_view(), name="univInfo"),
    path("targetInfo01/", TargetInfo01View.as_view(), name="targetInfo01"),
    path("targetInfo02/", TargetInfo02View.as_view(), name="targetInfo02"),
]