from django.test import TestCase
from accounts.models import Lesson, Profile
from .models import Favor, Search

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

User = get_user_model()


class TestCreateLessonView(TestCase):
    def setUp(self):
        self.url = reverse("matching:createLesson")
        user01 = User.objects.create_user(
            username="testuser01",
            email="testemail01@example.com",
            password="testpassword01",
        )
        Profile.objects.create(user=user01, univ_name="testuniv")
        self.client.login(username="testuser01", password="testpassword01")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "lesson_name": "testlesson",
            "day_of_week": 1,
            "time": 1,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("matching:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(
            Lesson.objects.filter(
                lesson_name="testlesson",
                univ_name="testuniv",
            ).count(),
            1,
        )

    def test_success_post_with_existing_lesson(self):
        data = {
            "lesson_name": "testlesson",
            "day_of_week": 1,
            "time": 1,
        }
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("matching:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(
            Lesson.objects.filter(
                lesson_name="testlesson",
                univ_name="testuniv",
            ).count(),
            1,
        )

'''
class TestSearchView(TestCase):
    def setUp(self):
        user01 = User.objects.create_user(
            username="username01",
            email="user01@example.com",
            password="username01password",
        )
        self.client.login(username="username01", password="username01password")
        user02 = User.objects.create_user(
            username="username02",
            email="user02@example.com",
            password="username02password",
        )
        profile01 = Profile.objects.create(
            user=user01,
            gender=0,
            grade=1,
            age=20,
            target=0,
            seconde_target=0,
            univ_name="tempuniv",
        )
        profile02 = Profile.objects.create(
            user=user02,
            gender=0,
            grade=1,
            age=20,
            target=0,
            seconde_target=0,
            univ_name="tempuniv"
        )
        lesson01 = Lesson.objects.create(
            user=user01,
            univ_name=profile01.univ_name,
            lesson_name="templesson",
            day_of_week=0,
            time=1,
        )
        favor01 = Favor.objects.create(
            user=user01,
            gender=0,
            grade=1,
            age="same",
            target=0,
            seconde_target=0,
            num_of_people=3,
        )
        favor02 = Favor.objects.create(
            user=user02,
            gender=0,
            grade=1,
            age="same",
            target=0,
            seconde_target=0,
            num_of_people=3,
        )
        Search01 = Search.objects.create(
            user=user01,
            lesson=lesson01,
            favor=favor01,
        )
        Search02 = Search.objects.create(
            user=user02,
            lesson=lesson01,
            favor=favor02,
        )
        search_id = Search01.id
        self.url = reverse("matching:search", kwargs={"search_id": search_id})
    
    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        

'''