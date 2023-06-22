from rest_framework.test import APITestCase
import factory
from django.urls import reverse
from django.contrib.auth.models import User
from user_manager.models import UserMetadata
from rest_framework.test import APITestCase, APIClient


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class UserRegistrationTests(APITestCase):
    def test_registration(self):
        password = factory.Faker("password")
        data = {
            "email": "fake@fake.com",
            "password": password,
            "password2": password,
        }

        auth_url = reverse("auth-register")
        response = self.client.post(auth_url, data)
        new_user = User.objects.filter(email=response.data["email"]).get()
        matching_metadata = UserMetadata.objects.filter(user=new_user).get()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        self.assertIsNotNone(matching_metadata.guid)

    def test_mismatch_passwords(self):
        data = {
            "email": "fake@fake.com",
            "password": factory.Faker("password"),
            "password2": factory.Faker("password"),
        }
        auth_url = reverse("auth-register")
        response = self.client.post(auth_url, data)

        self.assertEqual(response.status_code, 400)

    def test_duplicate_email(self):
        password = factory.Faker("password")
        data = {
            "email": "fake@fake.com",
            "password": password,
            "password2": password,
        }
        auth_url = reverse("auth-register")

        self.client.post(auth_url, data)

        response = self.client.post(auth_url, data)
        self.assertEqual(response.status_code, 400)

    def test_duplicate_preexisting_account(self):
        UserFactory(email="fake@fake.com")

        data = {
            "email": "fake@fake.com",
            "password": factory.Faker("password"),
            "password2": factory.Faker("password"),
        }
        auth_url = reverse("auth-register")
        response = self.client.post(auth_url, data)

        self.assertEqual(response.status_code, 400)


class UserTokenTests(APITestCase):
    def test_token(self):
        password = factory.Faker("password")
        data = {
            "email": "fake@fake.com",
            "password": password,
            "password2": password,
        }
        auth_url = reverse("auth-register")
        self.client.post(auth_url, data)

        data = {
            "username": "fake@fake.com",
            "password": password,
        }
        token_url = reverse("token")
        response = self.client.post(token_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data["token"])

    def test_user_details(self):
        password = factory.Faker("password")
        data = {
            "email": "fake@fake.com",
            "password": password,
            "password2": password,
        }

        auth_url = reverse("auth-register")
        self.client.post(auth_url, data)

        data = {
            "username": "fake@fake.com",
            "password": password,
        }
        token_url = reverse("token")
        response = self.client.post(token_url, data)
        token = response.data["token"]

        user_details_url = reverse("user-details")
        response = self.client.get(
            user_details_url, HTTP_AUTHORIZATION=f"Token {token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "fake@fake.com")


class UserLoginTests(APITestCase):
    def test_login(self):
        data = {
            "email": "hi@test.com",
            "password": "h4rryP0tt3r!",
        }

        User.objects.create_user(
            username=data["email"], email=data["email"], password=data["password"]
        )

        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        data = {
            "email": "hi@test.com",
            "password": "h4rryP0tt3r!",
        }

        User.objects.create_user(
            username=data["email"], email=data["email"], password=data["password"]
        )

        response = self.client.post(
            "/auth/login/", {"email": data["email"], "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 404)


class CheckValidCredentialsTests(APITestCase):
    def test_check_valid_credentials(self):
        data = {
            "email": "hi@test.com",
            "password": "h4rryP0tt3r!",
        }

        user = User.objects.create_user(
            username=data["email"], email=data["email"], password=data["password"]
        )

        # Check that the user in the request is authenticated
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/auth/check/")
        self.assertEqual(response.status_code, 200)
