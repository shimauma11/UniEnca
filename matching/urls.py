from django.urls import path
from .views import TempView

app_name = "matching"
urlpatterns = [
    path("", TempView, name="temp"),
]