from django.urls import path
from .views import (
    CreateRoomView,
    JoinRoomView,
    DMView,
    DMListView,
    LeaveRoomView,
)

app_name = "dm"
urlpatterns = [
    path(
        "createRoom/<int:search_id>/<int:this_search_id>/",
        CreateRoomView.as_view(),
        name="createRoom",
    ),
    path("joinRoom/<int:search_id>/<int:this_search_id>/", JoinRoomView.as_view(), name="joinRoom"),
    path("dm/<int:search_id>/", DMView.as_view(), name="dm"),
    path("dmList/", DMListView.as_view(), name="dmList"),
    path("leaveRoom/<int:search_id>/", LeaveRoomView.as_view(), name="leaveRoom"),
]
