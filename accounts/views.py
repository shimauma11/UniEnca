from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView as UserCreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.conf import settings

from .models import Profile, Hobby
from .forms import (
    LoginForm,
    BasicInfoForm,
    UnivInfoForm,
    TargetInfo01Form,
    SignupForm,
    CreateHobbyForm,
    BasicInfoEditForm,
    UnivInfoEditForm,
    ProfileTextEditForm,
)

# Create your views here.

User = get_user_model()


class WelcomeView(View):
    template_name = "accounts/welcome.html"

    def get(self, request):
        ctxt = {}
        return render(request, self.template_name, ctxt)


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


class UserLogoutView(LogoutView):
    pass


class BasicInfoView(View, LoginRequiredMixin):
    model = Profile
    form_class = BasicInfoForm
    template_name = "accounts/basicInfo.html"

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


class UnivInfoView(View, LoginRequiredMixin):
    model = Profile
    form_class = UnivInfoForm
    template_name = "accounts/univInfo.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user = self.request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            univ_name = form.cleaned_data["univ_name"]
            faculty = form.cleaned_data["faculty"]
            major = form.cleaned_data["major"]
            campus = form.cleaned_data["campus"]
            user.profile.univ_name = univ_name
            user.profile.faculty = faculty
            user.profile.major = major
            user.profile.campus = campus
            user.profile.save()
            return redirect("accounts:targetInfo01")
        return render(request, self.template_name, {"form": form})


class TargetInfo01View(View, LoginRequiredMixin):
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
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {"form": form})


class CreateHobbyView(View, LoginRequiredMixin):
    model = Hobby
    form_class = CreateHobbyForm
    template_name = "accounts/createHobby.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user = self.request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            hobby_name = form.cleaned_data["hobby_name"]
            hobby_kind = form.cleaned_data["hobby_kind"]
            hobby, created = Hobby.objects.get_or_create(
                hobby_name=hobby_name, hobby_kind=hobby_kind
            )
            user.profile.hobby.add(hobby)
            user.profile.save()
            return redirect("accounts:myProfile")
        return render(request, self.template_name, {"form": form})


class ProfileView(View, LoginRequiredMixin):
    model = User
    template_name = "accounts/profile.html"

    def get(self, request, user_id, search_id):
        user = get_object_or_404(User, pk=user_id)
        ctxt = {
            "target_user": user,
            "search_id": search_id,
        }
        return render(request, self.template_name, ctxt)


class MyProfileView(View, LoginRequiredMixin):
    model = User
    template_name = "accounts/myProfile.html"

    def get(self, request):
        ctxt = {
            "target_user": self.request.user,
        }
        return render(request, self.template_name, ctxt)


class SeeRecruitView(View, LoginRequiredMixin):
    template_name = "accounts/seeRecruit.html"

    def get(self, request):
        ctxt = {}
        return render(request, self.template_name, ctxt)


class BasicInfoEditView(View, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "accounts/basicInfoEdit.html"
    form_class = BasicInfoEditForm

    def get(self, request, profile_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, profile_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, pk=profile_id)
            nickname = form.cleaned_data["nickname"]
            gender = form.cleaned_data["gender"]
            grade = form.cleaned_data["grade"]
            age = form.cleaned_data["age"]
            profile.nickname = nickname
            profile.gender = gender
            profile.grade = grade
            profile.age = age
            profile.save()
            return redirect("accounts:myProfile")
        return render(request, self.template_name, {"form": form})

    def test_func(self):
        user = self.request.user
        return user == self.get_object().user

    def get_object(self):
        return self.request.user.profile


class UnivInfoEditView(View, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "accounts/univInfoEdit.html"
    form_class = UnivInfoEditForm

    def get(self, request, profile_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, profile_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, pk=profile_id)
            univ_name = form.cleaned_data["univ_name"]
            faculty = form.cleaned_data["faculty"]
            major = form.cleaned_data["major"]
            campus = form.cleaned_data["campus"]
            profile.univ_name = univ_name
            profile.faculty = faculty
            profile.major = major
            profile.campus = campus
            profile.save()
            return redirect("accounts:myProfile")
        return render(request, self.template_name, {"form": form})

    def test_func(self):
        user = self.request.user
        return user == self.get_object().user

    def get_object(self):
        return self.request.user.profile


class ProfileTextEditView(View, LoginRequiredMixin, UserPassesTestMixin):
    template_name = "accounts/profileTextEdit.html"
    form_class = ProfileTextEditForm

    def get(self, request, profile_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, profile_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            profile = get_object_or_404(Profile, pk=profile_id)
            profile_text = form.cleaned_data["profile_text"]
            profile.profile_text = profile_text
            profile.save()
            return redirect("accounts:myProfile")
        return render(request, self.template_name, {"form": form})

    def test_func(self):
        user = self.request.user
        return user == self.get_object().user

    def get_object(self):
        return self.request.user.profile
