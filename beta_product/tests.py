from django.test import TestCase
from beta_product.models import UserInterest, InterestFields
from django.contrib.auth.models import User


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
