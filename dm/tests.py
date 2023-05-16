from django.test import TestCase
from .models import Room, Message
from accounts.models import Lesson
from matching.models import Search, Recruit, Favor
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Create your tests here.

User = get_user_model()


class TestDMView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testemail01@example.com",
            password="testpassword01",
        )
        self.client.login(username="testuser01", password="testpassword01")
        self.room = Room.objects.create(name="testroom", max_num=1)
        self.room.members.add(self.user01)
        self.room.save()
        self.url = reverse("dm:dm", kwargs={"room_id": self.room.id})

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "body": "aaaaaaa",
            "sender": self.user01,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("dm:dm", kwargs={"room_id": self.room.id}),
            status_code=302,
            target_status_code=200,
        )
        self.assertTrue(Message.objects.exists())


class TestJoinRoomView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testemail01@example.com",
            password="testpassword01",
        )
        self.user02 = User.objects.create_user(
            username="testuser02",
            email="testemail02@example.com",
            password="testpassword02",
        )
        self.client.login(username="testuser01", password="testpassword01")

        self.lesson = Lesson.objects.create(
            lesson_name="testlesson",
            day_of_week=1,
            time=1,
            univ_name="testuniv",
        )
        self.lesson.students.add(self.user01)
        self.lesson.students.add(self.user02)

        self.favor01 = Favor.objects.create(
            user=self.user01, gender=1, grade=1, age=1, target=1
        )
        self.favor02 = Favor.objects.create(
            user=self.user02, gender=1, grade=1, age=1, target=1
        )

        self.search = Search.objects.create(
            user=self.user01,
            lesson=self.lesson,
            favor=self.favor01,
        )

        self.room = Room.objects.create(name="testroom", max_num=2)
        self.room.members.add(self.user02)
        self.room.save()

        self.recruit = Recruit.objects.create(
            user=self.user02,
            lesson=self.lesson,
            favor=self.favor02,
            room=self.room,
        )

        self.url = reverse(
            "dm:joinRoom",
            kwargs={
                "recruit_id": self.recruit.id,
                "search_id": self.search.id,
            },
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("dm:dm", kwargs={"room_id": self.room.id}),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Search.objects.exists())
        renew_room = get_object_or_404(Room, pk=self.room.id)
        self.assertEqual(renew_room.members.count(), 2)
        self.assertFalse(renew_room.can_join)


class TestLeaveRoomView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testemail01@example.com",
            password="testpassword01",
        )
        self.client.login(username="testuser01", password="testpassword01")

        self.lesson = Lesson.objects.create(
            lesson_name="testlesson",
            day_of_week=1,
            time=1,
            univ_name="testuniv",
        )
        self.lesson.students.add(self.user01)

        self.favor01 = Favor.objects.create(
            user=self.user01, gender=1, grade=1, age=1, target=1
        )

        self.room = Room.objects.create(name="testroom", max_num=1)
        self.room.members.add(self.user01)
        self.room.save()

        self.recruit = Recruit.objects.create(
            user=self.user01,
            lesson=self.lesson,
            favor=self.favor01,
            room=self.room,
        )

        self.url = reverse("dm:leaveRoom", kwargs={"room_id": self.room.id})

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse("matching:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Recruit.objects.exists())
        self.assertFalse(Favor.objects.exists())
        self.assertFalse(Room.objects.exists())


class TestRoomEditView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testemail01@example.com",
            password="testpassword01",
        )
        self.client.login(username="testuser01", password="testpassword01")
        self.room = Room.objects.create(name="testroom", max_num=1)
        self.room.members.add(self.user01)
        self.room.save()
        self.url = reverse("dm:roomEdit", kwargs={"room_id": self.room.id})

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {"name": "newname", "max_num": 5}
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("dm:dm", kwargs={"room_id": self.room.id}),
            status_code=302,
            target_status_code=200,
        )
        renew_room = get_object_or_404(Room, pk=self.room.id)
        self.assertEqual(renew_room.name, "newname")
        self.assertEqual(renew_room.max_num, 5)
