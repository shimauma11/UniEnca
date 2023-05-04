from typing import Optional
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden

from accounts.models import Lesson
from .models import Favor, Search
from .forms import CreateLessonForm, CreateFavorForm

# Create your views here.
User = get_user_model()


class HomeView(TemplateView, LoginRequiredMixin):
    template_name = "matching/home.html"


# Lessonインスタンスを作成または取得。
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
                # formに無い大学名とuserを追加
                lesson = form.save(commit=False)
                lesson.univ_name = univ_name
                lesson.save()
                lesson.students.add(user)
                form.save_m2m()
                lesson_id = lesson.id
            # すでにこのLessonインスタンスがある場合は、this_lessonとして再利用。
            this_lesson = get_object_or_404(
                Lesson, lesson_name=lesson_name, univ_name=univ_name
            )
            lesson_id = this_lesson.id
            this_lesson.students.add(user)
            # CreateFavorViewでもこのLessonインスタンスを使うため、lesson_idを渡す。
            url = reverse(
                "matching:createFavor", kwargs={"lesson_id": lesson_id}
            )
            return redirect(url)
        return render(request, self.template_name, {"form": form})


# Favorインスタンスを作成。このインスタンスを持つSearchインスタンスが削除された際に、このFavorも削除される。
class CreateFavorView(View, LoginRequiredMixin):
    model = Favor
    form_class = CreateFavorForm
    template_name = "matching/createFavor.html"

    def get(self, request, lesson_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, lesson_id):
        user = self.request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            favor = form.save(commit=False)
            gender = form.cleaned_data["gender"]
            age = form.cleaned_data["age"]
            grade = form.cleaned_data["grade"]
            num_of_people = form.cleaned_data["num_of_people"]
            target = user.profile.target
            second_target = user.profile.target
            favor, created = Favor.objects.get_or_create(
                gender=gender,
                age=age,
                grade=grade,
                num_of_people=num_of_people,
                target=target,
                second_target=second_target,
                user=user,
            )
            favor_id = favor.id
            url = reverse(
                "matching:createSearch",
                kwargs={"lesson_id": lesson_id, "favor_id": favor_id},
            )
            return redirect(url)
        return render(request, self.template_name, {"form": form})


# Searchインスタンスを作成、または取得
class CreateSearchView(View, LoginRequiredMixin):
    model = Search

    def get(self, request, lesson_id, favor_id):
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        favor = get_object_or_404(Favor, pk=favor_id)
        user = self.request.user
        # すでにある場合は、既存のSearchインスタンスを再利用する
        search, created = Search.objects.get_or_create(
            user=user, lesson=lesson, favor=favor
        )
        search_id = search.id
        # SearchViewで、このviewで作成したSearchインスタンスが必要になるため、search_idを渡す。
        url = reverse("matching:search", kwargs={"search_id": search_id})
        return redirect(url)


# search_listには、ログインユーザが作成したlessonインスタンスと同じインスタンスを持つSearchインスタンスのリストを入れる
class SearchView(View, LoginRequiredMixin):
    model = Search
    template_name = "matching/searchResult.html"

    def get(self, request, search_id):
        user = self.request.user
        this_search = get_object_or_404(Search, id=search_id)
        lesson = this_search.lesson
        favor = this_search.favor
        search_list = lesson.searches.all()
        ctxt = {}
        if not search_list:
            ctxt = {
                "searchList": search_list,
                "list_count": 0,
                "this_search": this_search,
            }
            return render(request, self.template_name, ctxt)
        result = narrowDown(
            search_list=search_list, favor=favor, request_user=user
        )
        count = list_count(result)
        ctxt = {
                "searchList": result,
                "list_count": count,
                "this_search": this_search,
            }
        return render(request, self.template_name, ctxt)


class DeleteSearchView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Search
    success_url = reverse_lazy("matching:home")
    template_name = "matching/deleteSearch.html"

    def test_func(self):
        self.object = self.get_object()
        return self.request.user == self.object.user

    def handle_no_permission(self):
        return HttpResponseForbidden("You aren't allowed to do this action.")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


"""
SearchView内で、lessonが同じSearchインスタンスのリストを受け取り、それをさらに絞り込むための関数。
ログインユーザのfavorと相手のprofileが一致しているか、またその逆も一致しているかを確認して、両方一致
していた場合のみ、そのSearchインスタンスをresultに入れる
↓
"""


def narrowDown(search_list, favor, request_user):
    result = []
    you = request_user.profile  # youはログインユーザ
    for search in search_list:
        partner = search.user.profile
        if search.user == request_user:  # 検索した時に自分のSearchも表示する必要がないため、この処理を行う
            continue
        # ログインユーザのfavorとpartnerのprofileの照合
        is_matched = judger(you=you, favor=favor, partner=partner)
        if is_matched:
            # partnerのfavorとログインユーザのprofileの照合
            if judger(you=partner, favor=search.favor, partner=you):
                # 双方一致したSearchインスタンスはresultに入れる
                result.append(search)
    return result


# 以下は、年齢、学年、性別の希望が一致しているか確かめるための関数。bool値で返す。
def judgeAge(you, partner, favor):
    if favor.age == "upper":
        if you.age < partner.age:
            return True

    if favor.age == "same":
        if you.age == partner.age:
            return True

    if favor.age == "lower":
        if you.age > partner.age:
            return True

    if favor.age == "whatever":
        return True


def judgeGrade(partner, favor):
    if favor.grade == 5:
        return True
    return favor.grade == partner.grade


def judgeGender(partner, favor):
    if favor.gender == 3:
        return True
    return favor.gender == partner.gender


# 全ての情報が一致しているかを確かめる関数。bool値で返す
def judger(you, partner, favor):
    result_age = judgeAge(you=you, partner=partner, favor=favor)
    result_grade = judgeGrade(partner=partner, favor=favor)
    result_gender = judgeGender(partner=partner, favor=favor)
    result_target = you.target == partner.target
    result_second_target = you.second_target == partner.second_target
    if (
        result_age
        and result_grade
        and result_gender
        and result_target
        and result_second_target
    ):
        return True
    return False


def list_count(search_list):
    count = 0
    for search in search_list:
        count += 1
    return count