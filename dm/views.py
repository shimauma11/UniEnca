from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse

from .forms import CreateRoomForm, MessageSendForm
from matching.models import Search
from .models import Room

User = get_user_model()


class CreateRoomView(View, LoginRequiredMixin):
    form_class = CreateRoomForm
    template_name = "dm/createRoom.html"

    def get(self, request, search_id, this_search_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, search_id, this_search_id):
        user = self.request.user
        this_search = get_object_or_404(Search, pk=this_search_id)
        search = get_object_or_404(Search, pk=search_id)
        partner = search.user
        lesson = search.lesson
        form = self.form_class(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.lesson = lesson
            room.save()
            room.members.add(user)
            room.members.add(partner)
            this_search.room = room
            search.room = room
            room.save()
            this_search.save()
            search.save()
            url = reverse("dm:dm", kwargs={"search_id": this_search_id})
            return redirect(url)
        return render(request, self.template_name, {"form": form})


class DMView(View, LoginRequiredMixin):
    template_name = "dm/dm.html"
    form_class = MessageSendForm

    def get(self, request, search_id):
        form = self.form_class()
        search = get_object_or_404(Search, pk=search_id)
        room = search.room
        messages = room.messages.all()
        ctxt = {
            "form": form,
            "messages": messages,
            "this_search": search,
        }
        return render(request, self.template_name, ctxt)

    def post(self, request, search_id):
        user = self.request.user
        form = self.form_class(request.POST)
        search = get_object_or_404(Search, pk=search_id)
        room = search.room
        messages = room.messages.all()
        ctxt = {
            "form": form,
            "messages": messages,
            "this_search": search,
        }
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.room = room
            message.save()
            url = reverse("dm:dm", kwargs={"search_id": search_id})
            return redirect(url)
        return render(request, self.template_name, ctxt)


class DMListView(TemplateView, LoginRequiredMixin):
    template_name = "dm/dmList.html"


class JoinRoomView(View, LoginRequiredMixin):
    template_name = "dm/temp.html"

    def get(self, request, search_id, this_search_id):
        search = get_object_or_404(Search, pk=search_id)
        this_search = get_object_or_404(Search, pk=this_search_id)
        user = self.request.user
        room = search.room
        room.members.add(user)
        room.save()
        this_search.room = room
        this_search.save()
        url = reverse("dm:dm", kwargs={"search_id": this_search_id})
        return redirect(url)


class LeaveRoomView(View, LoginRequiredMixin):
    def get(self, request, search_id):
        search = get_object_or_404(Search, pk=search_id)
        user = self.request.user
        room = search.room
        room.members.remove(user)
        room.save()
        search.room = None
        search.save()
        return redirect("matching:home")
