from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from accounts.models import Lesson
from .models import Favor, Search, Recruit
from dm.models import Room
from .forms import CreateLessonForm, CreateFavorForm
from dm.forms import RoomEditForm

# Create your views here.
User = get_user_model()


class HomeView(TemplateView, LoginRequiredMixin):
    template_name = "matching/home.html"


# Lessonインスタンスを作成または取得。
class CreateLessonView(View, LoginRequiredMixin):
    model = Lesson
    form_class = CreateLessonForm
    template_name = "matching/createLesson.html"

    def get(self, request, path):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, path):
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
                if path == "recruit":
                    lesson.students.add(user)
                    form.save_m2m()
                lesson_id = lesson.id
            # すでにこのLessonインスタンスがある場合は、this_lessonとして再利用。
            this_lesson = get_object_or_404(
                Lesson, lesson_name=lesson_name, univ_name=univ_name
            )
            lesson_id = this_lesson.id
            if path == "recruit":
                this_lesson.students.add(user)
            # CreateFavorViewでもこのLessonインスタンスを使うため、lesson_idを渡す。
            url = reverse(
                "matching:createFavor",
                kwargs={"lesson_id": lesson_id, "path": path},
            )
            return redirect(url)
        return render(request, self.template_name, {"form": form})


# すでに同じFavorインスタンスがある場合もFavorを作成。削除の際、Favorの重複を許さないと、複数のSearchが消えてしまうため
class CreateFavorView(View, LoginRequiredMixin):
    model = Favor
    form_class = CreateFavorForm
    template_name = "matching/createFavor.html"

    def get(self, request, lesson_id, path):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, lesson_id, path):
        user = self.request.user
        form = self.form_class(request.POST)
        if form.is_valid():
            # すでに同じfavorがあるかどうかをチェックするための情報
            gender = form.cleaned_data["gender"]
            grade = form.cleaned_data["grade"]
            age = form.cleaned_data["age"]
            target = user.profile.target

            favor, created = Favor.objects.get_or_create(
                user=user,
                gender=gender,
                grade=grade,
                age=age,
                target=target,
            )
            favor.save()

            favor_id = favor.id
            if path == "search":
                url = reverse(
                    "matching:createSearch",
                    kwargs={"lesson_id": lesson_id, "favor_id": favor_id},
                )
            else:
                url = reverse(
                    "matching:createRecruit",
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
    model = Recruit
    template_name = "matching/searchResult.html"

    def get(self, request, search_id):
        user = self.request.user
        this_search = get_object_or_404(Search, id=search_id)
        lesson = this_search.lesson
        favor = this_search.favor
        recruit_list = list(lesson.recruites.filter(room__can_join=True))
        # lessonが1つもrecruitを持っていない場合
        if not recruit_list:
            ctxt = {
                "recruitList": recruit_list,
                "list_count": 0,
                "this_search": this_search,  # 必要か後でチェック
            }
            return render(request, self.template_name, ctxt)
        # lessonがrecruitを持っている時。favorを元にさらにrecruitを絞る
        recruit_list = narrowDown(
            recruit_list=recruit_list, user_favor=favor, request_user=user
        )
        # 要修正
        count = len(recruit_list)
        ctxt = {
            "recruitList": recruit_list,
            "list_count": count,
            "this_search": this_search,
        }
        return render(request, self.template_name, ctxt)


class CreateRecruitView(View, LoginRequiredMixin):
    model = Room
    form_class = RoomEditForm
    template_name = "matching/createRecruit.html"

    def get(self, request, lesson_id, favor_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    # room作成と同時にrecruitを作成。roomのメンバーにログインユーザーを追加する。
    def post(self, request, lesson_id, favor_id):
        user = self.request.user
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        favor = get_object_or_404(Favor, pk=favor_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            room = form.save()
            room.members.add(user)
            room.save()
            recruit, created = Recruit.objects.get_or_create(
                user=user, lesson=lesson, favor=favor, room=room
            )
            url = reverse("dm:dm", kwargs={"room_id": room.id})
            return redirect(url)
        return render(request, self.template_name, {"form": form})


# ホームにリダイレクトされる
class DeleteFavorView(DeleteView, LoginRequiredMixin):
    model = Favor
    success_url = reverse_lazy("matching:home")
    template_name = "matching/delete.html"


"""
SearchView内で、lessonが同じSearchインスタンスのリストを受け取り、それをさらに絞り込むための関数。
ログインユーザのfavorと相手のprofileが一致しているか、またその逆も一致しているかを確認して、両方一致
していた場合のみ、そのSearchインスタンスをresultに入れる
↓
"""


def narrowDown(recruit_list, user_favor, request_user):
    result = []
    you = request_user.profile  # youはログインユーザ
    for recruit in recruit_list:
        room_info = createRoomInfo(recruit)
        # userのプロファイルとマッチしているrecruitのみを表示する
        recruit_favor = recruit.favor
        if (
            request_user in recruit.room.members.all()
        ):  # 自分自身がすでに参加しているrecruitは表示する必要がないため
            continue
        # recruitのFavorがrequest_userのprofileとマッチしているかを見る
        if judger(you=you, recruit_favor=recruit_favor):
            # かつ、検索しているuserのfavor.genderとfavor.gradeが、room_infoのgender,gradeとマッチしているかをチェック
            if user_favor.gender == 3:
                judge_gender = True
            else:
                judge_gender = room_info["gender"] == user_favor.gender

            if user_favor.grade == 5:
                judge_grade = True
            else:
                judge_grade = room_info["grade"] == user_favor.grade

            judge_target = user_favor.target == recruit_favor.target

            if judge_gender and judge_grade and judge_target:
                # マッチしているものはresultに入れて返す
                result.append(recruit)
    return result


# 以下は、年齢、学年、性別の希望が一致しているか確かめるための関数。bool値で返す。
def judgeAge(you, recruit_favor):
    if recruit_favor.age == "upper":
        if you.age < recruit_favor.age:
            return True

    if recruit_favor.age == "same":
        if you.age == recruit_favor.age:
            return True

    if recruit_favor.age == "lower":
        if you.age > recruit_favor.age:
            return True

    if recruit_favor.age == "whatever":
        return True


def judgeGrade(you, recruit_favor):
    if recruit_favor.grade == 5:
        return True
    return recruit_favor.grade == you.grade


def judgeGender(you, recruit_favor):
    if recruit_favor.gender == 3:
        return True
    return recruit_favor.gender == you.gender


# 全ての情報が一致しているかを確かめる関数。bool値で返す
def judger(you, recruit_favor):
    result_age = judgeAge(you, recruit_favor)
    result_grade = judgeGrade(you, recruit_favor)
    result_gender = judgeGender(you, recruit_favor)
    result_target = you.target == recruit_favor.target
    # favor全てマッチしていたらTrueを返す。違ったらFalseを返す。
    if result_age and result_grade and result_gender and result_target:
        return True
    return False


# roomの男女比,学年比率, 平均年齢などの情報を持つroom_infoを作る関数。
def createRoomInfo(recruit):
    # 比率の計算に必要な数字
    roomMembers = recruit.room.members
    allMembers = roomMembers.count()
    members_info = createMemberInfo(members=roomMembers)

    # それぞれの比率
    male_ratio = members_info["maleMember"] / allMembers * 100
    female_ratio = members_info["femaleMember"] / allMembers * 100
    other_gender_ratio = members_info["otherGenderMember"] / allMembers * 100
    grade1_ratio = members_info["grade1Member"] / allMembers * 100
    grade2_ratio = members_info["grade2Member"] / allMembers * 100
    grade3_ratio = members_info["grade3Member"] / allMembers * 100
    grade4_ratio = members_info["grade4Member"] / allMembers * 100

    # 性別、学年それぞれの中で最も割合が大きいものを探す
    max_gender = max(male_ratio, female_ratio, other_gender_ratio)

    if max_gender == male_ratio:
        gender = 0
    elif max_gender == female_ratio:
        gender = 1
    else:
        gender = 2
    print(gender)

    max_grade = max(grade1_ratio, grade2_ratio, grade3_ratio, grade4_ratio)

    if max_grade == grade1_ratio:
        grade = 1
    elif max_grade == grade2_ratio:
        grade = 2
    elif max_grade == grade3_ratio:
        grade = 3
    else:
        grade = 4

    room_info = {
        "male_ratio": male_ratio,
        "female_ratio": female_ratio,
        "otherGenderMember": other_gender_ratio,
        "grade1_ratio": grade1_ratio,
        "grade2_ratio": grade2_ratio,
        "grade3_ratio": grade3_ratio,
        "grade4_ratio": grade4_ratio,
        "gender": gender,
        "grade": grade,
    }
    return room_info


# room member比率計算に必要な数字を返す
def createMemberInfo(members):
    members_info = {
        "maleMember": 0,
        "femaleMember": 0,
        "otherGenderMember": 0,
        "grade1Member": 0,
        "grade2Member": 0,
        "grade3Member": 0,
        "grade4Member": 0,
    }
    for member in members.all():
        member = member.profile

        if member.gender == 0:
            members_info["maleMember"] += 1
        if member.gender == 1:
            members_info["femaleMember"] += 1
        else:
            members_info["otherGenderMember"] += 1

        if member.grade == 0:
            members_info["grade1Member"] += 1
        if member.grade == 1:
            members_info["grade2Member"] += 1
        if member.grade == 2:
            members_info["grade3Member"] += 1
        else:
            members_info["grade4Member"] += 1
    return members_info
