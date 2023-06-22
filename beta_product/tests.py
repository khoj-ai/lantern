from django.test import TestCase
from beta_product.models import UserInterest, InterestFields
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class BetaProductUserInterestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserInterest

    user = factory.SubFactory(User)
    field = factory.Faker("random_element", elements=InterestFields.values)
    waitlist = factory.Faker("boolean")
    unique_identifier = factory.Faker("uuid4")


class BetaProductUserInterest(TestCase):
    def test_user_interest(self):
        user = User.objects.create_user(username="test")
        user_interest = UserInterest.objects.create(field=InterestFields.ART, user=user)
        self.assertEqual(user_interest.field, InterestFields.ART)
        self.assertEqual(user_interest.user, user)

    def test_no_duplicates(self):
        user = User.objects.create_user(username="test")
        UserInterest.objects.create(field=InterestFields.ART, user=user)
        with self.assertRaises(Exception):
            UserInterest.objects.create(field=InterestFields.ART, user=user)


class BetaProductUserValidIdentifier(APITestCase):
    def test_is_valid_identifier(self):
        user = User.objects.create_user(username="test", email="test")

        user_interest = BetaProductUserInterestFactory(user=user)

        response = self.client.get(f"/beta/invite/{user_interest.unique_identifier}/")
        user_interest.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(user_interest.waitlist, False)

    def test_is_valid_identifier_already_set(self):
        user = UserFactory()

        user_interest = BetaProductUserInterestFactory(user=user)

        response = self.client.get(f"/beta/invite/{user_interest.unique_identifier}/")

        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertEqual(response.data, {})

    def test_is_not_valid_identifier(self):
        response = self.client.get(f"/beta/invite/1234/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {})


class BetaProductUserSetPassword(APITestCase):
    def test_set_password(self):
        user = User.objects.create_user(username="test", email="test")
        user_interest = BetaProductUserInterestFactory(user=user)
        response = self.client.post(
            f"/beta/invite/{user_interest.unique_identifier}/set-password/",
            {"password": "H4rryP0tt3r"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password("H4rryP0tt3r"))

    def test_set_password_already_set(self):
        user = UserFactory()
        user_interest = BetaProductUserInterestFactory(user=user)
        response = self.client.post(
            f"/beta/invite/{user_interest.unique_identifier}/set-password/",
            {"password": "test1234"},
        )

        self.assertEqual(response.status_code, status.HTTP_410_GONE)
        self.assertEqual(response.data, {})

    def test_set_password_invalid_identifier(self):
        response = self.client.post(
            f"/beta/invite/1234/set-password/", {"password": "test1234"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {})
