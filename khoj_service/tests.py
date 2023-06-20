from rest_framework.test import APITestCase
import factory
from django.contrib.auth.models import User
from khoj_service.models import RoutingTable
from unittest.mock import patch


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class UserRoutesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoutingTable

    user = factory.SubFactory(UserFactory)
    url = factory.Faker("url")


class UserKhojRenderTest(APITestCase):
    @patch("khoj_service.views.requests.get")
    def test_khoj_service_access(self, mock_get):
        user = UserFactory()
        UserRoutesFactory(user=user)
        self.client.force_authenticate(user=user)
        mock_get.return_value.status_code = 200

        response = self.client.get("/khoj/")

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_access(self):
        response = self.client.get("/khoj/")
        self.assertEqual(response.status_code, 401)

    def test_khoj_service_route_missing(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get("/khoj/")
        self.assertEqual(response.status_code, 404)


class UserKhojApiTest(APITestCase):
    @patch("khoj_service.views.requests.get")
    def test_khoj_service_api_access(self, mock_get):
        user = UserFactory()
        UserRoutesFactory(user=user)
        self.client.force_authenticate(user=user)
        mock_get.return_value.status_code = 200
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
