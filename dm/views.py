from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import MessageSendForm, RoomEditForm
from matching.models import Search, Recruit
from .models import Room

User = get_user_model()


class DMView(View, LoginRequiredMixin):
    template_name = "dm/dm.html"
    form_class = MessageSendForm

    def get(self, request, room_id):
        form = self.form_class()
        room = get_object_or_404(Room, pk=room_id)
        ctxt = {
            "form": form,
            "room": room,
            "room_id": room_id,
        }
        return render(request, self.template_name, ctxt)

    def post(self, request, room_id):
        user = self.request.user
        form = self.form_class(request.POST)
        room = get_object_or_404(Room, pk=room_id)
        ctxt = {
            "form": form,
            "room": room,
            "room_id": room_id,
        }
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.room = room
            message.save()
            url = reverse("dm:dm", kwargs={"room_id": room_id})
            return redirect(url)
        return render(request, self.template_name, ctxt)


class DMListView(TemplateView, LoginRequiredMixin):
    template_name = "dm/dmList.html"


class JoinRoomView(View, LoginRequiredMixin):
    def get(self, request, recruit_id, search_id):
        user = self.request.user
        recruit = get_object_or_404(Recruit, pk=recruit_id)
        # roomに加わった際もsearchとfavorが消える
        search = get_object_or_404(Search, pk=search_id)
        search.favor.delete()
        search.delete()
        room = recruit.room
        room.members.add(user)
        room.save()
        # 　定員に達した場合、検索に引っ掛からなくなる
        if room.max_num <= room.members.count():
            room.can_join = False
            room.save()
        room_id = room.id
        url = reverse("dm:dm", kwargs={"room_id": room_id})
        return redirect(url)


class LeaveRoomView(View, LoginRequiredMixin):
    def get(self, request, room_id):
        user = self.request.user
        room = get_object_or_404(Room, pk=room_id)
        room.members.remove(user)
        room.save()
        # 定員よりメンバーが少なくなれば、再度検索時に引っかかるようにする
        if room.max_num > room.members.count():
            room.can_join = True
            room.save()
        # ルームメンバーが1人もいなくなったらrecruit,favor,roomを消す
        if room.members.count() == 0:
            recruit = room.recruit
            recruit.favor.delete()
            recruit.delete()
            room.delete()
        return redirect("matching:home")


class RoomEditView(View, LoginRequiredMixin):
    form_class = RoomEditForm
    template_name = "dm/roomEdit.html"

    def get(self, request, room_id):
        form = self.form_class()
        ctxt = {
            "form": form,
            "room_id": room_id,
        }
        return render(request, self.template_name, ctxt)

    def post(self, request, room_id):
        form = self.form_class(request.POST)
        ctxt = {
            "form": form,
            "room_id": room_id,
        }
        if form.is_valid():
            new_name = form.cleaned_data["name"]
            new_max_num = form.cleaned_data["max_num"]
            room = get_object_or_404(Room, pk=room_id)
            room.name = new_name
            room.max_num = new_max_num
            room.save()
            url = reverse("dm:dm", kwargs={"room_id": room_id})
            return redirect(url)
        return render(request, self.template_name, ctxt)
