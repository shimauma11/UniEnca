from django.test import TestCase
from accounts.models import Lesson, Profile, Hobby

from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

User = get_user_model()


class TestCreateHobbyView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:createHobby")
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
            "hobby_name": "testhobby",
            "hobby_kind": 0,
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("matching:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(
            Hobby.objects.filter(
                hobby_name="testhobby",
                hobby_kind=0,
            ).count(),
            1,
        )

    def test_success_post_with_existing_post(self):
        data = {
            "hobby_name": "testhobby",
            "hobby_kind": 0,
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
            Hobby.objects.filter(
                hobby_name="testhobby",
                hobby_kind=0,
            ).count(),
            1,
        )
