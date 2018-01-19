import json

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer


class RestaurantListTest(APITestCase):
    def setUp(self):
        self.restaurant_1 = Restaurant.objects.create(name='Eleven Madison Park', opens_at='17:30:00', closes_at='22:30:00')
        self.restaurant_2 = Restaurant.objects.create(name='Osteria Francescana', opens_at='12:30:00', closes_at='13:30:00')

    def test_restaurants_list(self):
        url = reverse('restaurant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 2)
        self.assertEqual(json.loads(response.content), [
            {
                'id': self.restaurant_1.id,
                'name': 'Eleven Madison Park',
                'opens_at': '17:30:00',
                'closes_at': '22:30:00'
            },
            {
                'id': self.restaurant_2.id,
                'name': 'Osteria Francescana',
                'opens_at': '12:30:00',
                'closes_at': '13:30:00'
            }
        ])

    def test_create_restaurant_with_empty_input(self):
        url = reverse('restaurant-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_create_restaurant_with_valid_input(self):
        url = reverse('restaurant-list')
        data = {
            'name': 'El Celler de Can Roca',
            'opens_at': '13:00:00',
            'closes_at': '23:00:00'
        }
        response = self.client.post(url, data, format='json')
        new_restaurant = Restaurant.objects.latest('id')
        data['id'] = new_restaurant.id
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 3)
        self.assertEqual(RestaurantSerializer(new_restaurant).data, data)

    def test_create_restaurant_with_invalid_input_1(self):
        url = reverse('restaurant-list')
        data = {
            'name': """                  THIS TEXT IS OVER 256 CHARACTERS
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
                    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud
                    exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute
                    irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
                    pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                    deserunt mollit anim id est laborum.""",
            'opens_at': '13:00:00',
            'closes_at': '23:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_create_restaurant_with_invalid_input_2(self):
        url = reverse('restaurant-list')
        data = {
            'name': 'Restaurant with wrong opening times.',
            'opens_at': '23:00:00',
            'closes_at': '12:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_create_restaurant_with_missing_field(self):
        url = reverse('restaurant-list')
        data = {
            'name': 'Restaurant without a field.',
            'closes_at': '23:00:00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 2)


class RestaurantDetailTest(APITestCase):
    def setUp(self):
        self.restaurant_1 = Restaurant.objects.create(name='Mirazur', opens_at='12:15:00', closes_at='14:15:00')

    def test_get_restaurant_details(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(response.data,
            {
                'id': self.restaurant_1.id,
                'name': 'Mirazur',
                'opens_at': '12:15:00',
                'closes_at': '14:15:00'
            }
        )

    def test_get_unexisting_restaurant_details(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_update_restaurant_details(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id})
        data = {
            'name': 'New Mirazur that closes later',
            'opens_at': '12:15:00',
            'closes_at': '14:16:00'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(response.data,
            {
                'id': self.restaurant_1.id,
                'name': 'New Mirazur that closes later',
                'opens_at': '12:15:00',
                'closes_at': '14:16:00'
            }
        )

    def test_update_restaurant_details_invalid_input(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id})
        data = {
            'name': 'New Mirazur that closes before it opens',
            'opens_at': '14:15:00',
            'closes_at': '12:15:00'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertNotEqual(RestaurantSerializer(self.restaurant_1),
            {
                'id': self.restaurant_1.id,
                'name': 'New Mirazur that closes later',
                'opens_at': '12:15:00',
                'closes_at': '14:16:00'
            }
        )

    def test_update_unexisting_restaurant_details(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id + 1})
        data = {
            'name': 'New Mirazur that closes later',
            'opens_at': '12:15:00',
            'closes_at': '14:16:00'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_delete_restaurant(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Restaurant.objects.count(), 0)

    def test_delete_unexisting_restaurant(self):
        url = reverse('restaurant-details', kwargs={'pk': self.restaurant_1.id + 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Restaurant.objects.count(), 1)
