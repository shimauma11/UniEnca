from django.urls import path
from .views import (
    JoinRoomView,
    DMView,
    DMListView,
    LeaveRoomView,
    RoomEditView,
)

app_name = "dm"
urlpatterns = [
    path(
        "joinRoom/<int:recruit_id>/<int:search_id>/",
        JoinRoomView.as_view(),
        name="joinRoom",
    ),
    path("dm/<int:room_id>/", DMView.as_view(), name="dm"),
    path("dmList/", DMListView.as_view(), name="dmList"),
    path(
        "leaveRoom/<int:room_id>/", LeaveRoomView.as_view(), name="leaveRoom"
    ),
    path("roomEdit/<int:room_id>/", RoomEditView.as_view(), name="roomEdit"),
]
