from django.test import TestCase

from restaurants.models import Restaurant, Category, Product, RestaurantCategory
from users.models import User


class ModelsTestCase(TestCase):
    def setUp(self):
        rest = Restaurant.objects.create(
            title="Rest",
            description="description",
            phone="89999999999",
            address="Test street, 22",
            delivery_time=90,
            delivery_min=100,
        )
        User.objects.create(
            email="test@example.com",
            password="test",
            restaurant=rest,
            role=User.RoleTypeChoices.MANAGER
        )

        c = RestaurantCategory.objects.create(category=Category.objects.create(name="cat"), restaurant=rest)
        Product.objects.create(title="Shaverma", description="food of gods", restaurant_category=c, price=199)

    def test_restaurant(self):
        rest = Restaurant.objects.get(title="Rest")
        rest_user = User.objects.get(email="test@example.com")
        self.assertEqual(rest.title, "Rest")
        self.assertEqual(rest.description, "description")
        self.assertEqual(rest.phone, "89999999999")
        self.assertEqual(rest.logo, '')
        self.assertEqual(rest.address, "Test street, 22")
        self.assertEqual(rest.delivery_min, 100)
        self.assertEqual(rest.delivery_time, 90)
        self.assertIsNone(rest.self_pickup_discount)
        self.assertIn(rest_user, rest.users.all())
        self.assertEqual(rest.users.get(email="test@example.com"), rest_user)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_category(self):
        c = RestaurantCategory.objects.get(category__name="cat")
        self.assertEqual(c.category.name, "cat")
        self.assertEqual(c.restaurant.title, "Rest")
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_product(self):
        p = Product.objects.get(title="Shaverma")
        self.assertEqual(p.title, "Shaverma")
        self.assertEqual(p.description, "food of gods")
        self.assertEqual(str(p.restaurant_category.category), "cat")
        self.assertIsNone(p.weight)
        self.assertEqual(p.price, 199)
        self.assertTrue(p.is_available)
        self.assertEqual(Product.objects.count(), 1)
