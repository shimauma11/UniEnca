from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView as UserCreateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

from .models import Profile, Univ
from .forms import LoginForm, BasicInfoForm, UnivInfoForm, TargetInfo01Form, TargetInfo02Form, SignupForm
# Create your views here.

User = get_user_model()


class SignupView(UserCreateView):
    model = User
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("accounts:basicInfo")

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm


class BasicInfoView(View):
    model = Profile
    form_class = BasicInfoForm
    template_name = "accounts/BasicInfo.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            user = self.request.user
            profile.user = user
            profile.save()
            return redirect("accounts:univInfo")
        return render(request, self.template_name, {"form": form})


class UnivInfoView(View):
    model = Univ
    form_class = UnivInfoForm
    template_name = "accounts/UnivInfo.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            univ = form.save(commit=False)
            user = self.request.user
            univ.user = user
            univ.save()
            return redirect("accounts:targetInfo01")
        return render(request, self.template_name, {"form": form})


class TargetInfo01View(View):
    model = Profile
    form_class = TargetInfo01Form
    template_name = "accounts/targetInfo01.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user = self.request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            user.profile.target = form.cleaned_data["target"]
            user.profile.save()
            return redirect("accounts:targetInfo02")
        return render(request, self.template_name, {"form": form})


class TargetInfo02View(View):
    model = Profile
    form_class = TargetInfo02Form
    template_name = "accounts/targetInfo02.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user = self.request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            user.profile.second_target = form.cleaned_data["second_target"]
            user.profile.save()
            return redirect("accounts:login")
        return render(request, self.template_name, {"form": form})