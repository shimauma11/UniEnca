from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Lesson
from .forms import CreateLessonForm

# Create your views here.


class HomeView(TemplateView, LoginRequiredMixin):
    template_name = "matching/home.html"


class CreateLessonView(View, LoginRequiredMixin):
    model = Lesson
    form_class = CreateLessonForm
    template_name = "matching/createLesson.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        user = self.request.user
        univ_name = user.profile.univ_name
        form = self.form_class(request.POST)
        if form.is_valid():
            lesson_name = form.cleaned_data["lesson_name"]
            exist = Lesson.objects.filter(
                lesson_name=lesson_name, univ_name=univ_name
            ).exists()
            if not exist:
                lesson = form.save(commit=False)
                lesson.univ_name = univ_name
                lesson.save()
                lesson.students.add(user)
                form.save_m2m()
                return redirect("matching:home")

            this_lesson = get_object_or_404(
                Lesson, lesson_name=lesson_name, univ_name=univ_name
            )
            this_lesson.students.add(user)
            return redirect("matching:home")

        return render(request, self.template_name, {"form": form})
