from rest_framework import status
from rest_framework import status
from rest_framework.test import APITestCase

from restaurants.models import Restaurant
from users.models import User


class RestaurantViewTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = {
            "title": "Test rest",
            "description": "description",
            "phone": "89999999999",
            "delivery_min": 777,
            "delivery_time": 10,
            "self_pickup_discount": 20
        }
        cls.rest = Restaurant.objects.create(**cls.data)
        cls.user = User.objects.create(email="user@example.com", role="customer")
        cls.manager = User.objects.create(email="manager@example.com", role="manager", restaurant=cls.rest)
        cls.superuser = User.objects.create(email="superuser@example.com", is_superuser=True, is_staff=True)

    def test_create_restaurant(self):
        # Only a superuser can create new restaurant
        data = {**self.data, 'title': 'New Rest'}
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/restaurants/r/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Superuser can create a new restaurant
        self.client.force_authenticate(self.superuser)
        response = self.client.post('/restaurants/r/', data)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['phone'], data['phone'])
        self.assertEqual(response.data['delivery_min'], data['delivery_min'])
        self.assertEqual(response.data['delivery_time'], data['delivery_time'])
        self.assertEqual(response.data['self_pickup_discount'], data['self_pickup_discount'])
        self.assertIsNone(response.data['logo'])
        self.assertIsNone(response.data['address'])

        # Unique
        response = self.client.post('/restaurants/r/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Phone max length
        data = self.data.copy()
        data['phone'] = "8999999999999"
        response = self.client.post('/restaurants/r/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        del data['phone']
        del data['title']
        response = self.client.post('/restaurants/r/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_restaurant(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/restaurants/r/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['title'], self.data['title'])

    def test_update_restaurant(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch('/restaurants/r/1/', {'title': "new title"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.manager)
        response = self.client.patch('/restaurants/r/1/', {'title': "new title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "new title")

        self.client.force_authenticate(self.superuser)
        response = self.client.put('/restaurants/r/1/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.data['title'])

    def test_destroy_restaurant(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete('/restaurants/r/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.manager)
        response = self.client.delete('/restaurants/r/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.superuser)
        self.client.delete('/users/2/')
        response = self.client.delete('/restaurants/r/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
