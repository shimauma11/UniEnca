from django.test import TestCase
from .models import Lesson, Profile, Hobby
from matching.models import Favor, Search


from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.

User = get_user_model()


class TestCreateHobbyView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:createHobby")
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testemail01@example.com",
            password="testpassword01",
        )
        Profile.objects.create(user=self.user01, univ_name="testuniv")
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
            reverse("accounts:myProfile"),
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
            reverse("accounts:myProfile"),
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


class TestProfileView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testuserpassword01",
        )
        self.client.login(username="testuser01", password="testuserpassword01")
        self.user02 = User.objects.create_user(
            username="testuser02",
            email="testuser02@example.com",
            password="testuserpassword02",
        )
        self.favor = Favor.objects.create(
            user=self.user01,
            gender=0,
            grade=1,
            age=20,
            target=1,
        )
        self.lesson = Lesson.objects.create(
            lesson_name="templesson", univ_name="tempuniv"
        )
        self.search = Search.objects.create(
            user=self.user01,
            lesson=self.lesson,
            favor=self.favor,
        )
        self.url = reverse(
            "accounts:profile",
            kwargs={"user_id": self.user02.id, "search_id": self.search.id},
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestMyProfileView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testuserpassword01",
        )
        self.profile01 = Profile.objects.create(
            user=self.user01,
            univ_name="tempuniv",
        )
        self.client.login(username="testuser01", password="testuserpassword01")
        self.url = reverse("accounts:myProfile")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestSeeRecruitView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testuserpassword01",
        )
        self.client.login(username="testuser01", password="testuserpassword01")
        self.url = reverse("accounts:seeRecruit")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class BasicInfoEditView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testuserpassword01",
        )
        self.profile01 = Profile.objects.create(
            user=self.user01,
            nickname="tempname",
            univ_name="tempuniv",
            profile_text="temptext",
        )
        self.client.login(username="testuser01", password="testuserpassword01")
        self.url = reverse(
            "accounts:basicInfoEdit", kwargs={"profile_id": self.profile01.id}
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "nickname": "newname",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("accounts:myProfile"),
            status_code=302,
            target_status_code=200,
        )


class TestUnivInfoEditView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testuserpassword01",
        )
        self.profile01 = Profile.objects.create(
            user=self.user01,
            nickname="tempname",
            univ_name="tempuniv",
            profile_text="temptext",
        )
        self.client.login(username="testuser01", password="testuserpassword01")
        self.url = reverse(
            "accounts:univInfoEdit", kwargs={"profile_id": self.profile01.id}
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {"univ_name": "newunivname"}
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response,
            reverse("accounts:myProfile"),
            status_code=302,
            target_status_code=200,
        )


class TestProfileTextEditView(TestCase):
    def setUp(self):
        self.user01 = User.objects.create_user(
            username="testuser01",
            email="testuser01@example.com",
            password="testuserpassword01",
        )
        self.profile01 = Profile.objects.create(
            user=self.user01,
            nickname="tempname",
            univ_name="tempuniv",
            profile_text="temptext",
        )
        self.client.login(username="testuser01", password="testuserpassword01")
        self.url = reverse(
            "accounts:profileTextEdit", kwargs={"profile_id": self.profile01.id}
        )

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "profile_text": "newprofiletext"
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(
            response, 
            reverse("accounts:myProfile"),
            status_code=302,
            target_status_code=200,
        )