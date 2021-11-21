from django.contrib.auth import authenticate
from django.test import TestCase

from restaurants.models import Restaurant
from users.models import User


class UserTestCase(TestCase):
    def setUp(self):
        rest = Restaurant.objects.create(
            title="Rest",
            description="description",
            phone="89999999999",
            address="Test street, 22",
            delivery_time=90,
            delivery_min=100,
        )
        User.objects.create_user(
            username="test",
            email="test@example.com",
            password="test123",
            phone="89000000000",
            restaurant=rest,
            role=User.RoleTypeChoices.MANAGER
        )

    def test_user(self):
        u = User.objects.get(email="test@example.com")
        self.assertEqual(u.username, "test")
        self.assertEqual(u.email, "test@example.com")
        self.assertEqual(u.phone, "89000000000")
        self.assertEqual(u.role, 'manager')
        self.assertEqual(u.restaurant.title, "Rest")

    def test_authenticate_user(self):
        user = authenticate(email="test@example.com", password="test123")
        self.assertIsNotNone(user)
        user = authenticate(email="test@example.com", password="test1223")
        self.assertIsNone(user)
