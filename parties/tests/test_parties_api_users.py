from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from parties.models import User


class UsersSuperuserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_users_view(self):
        url = reverse('api:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for user in response.data:
            user_url = user.get('url')
            response_user_get = self.client.get(user_url)
            self.assertEqual(response_user_get.status_code, status.HTTP_200_OK)

class UsersUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_users_view_permissions(self):
        url = reverse('api:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for user in response.data:
            user_url = user.get('url')
            response_user_get = self.client.get(user_url)
            self.assertEqual(response_user_get.status_code, status.HTTP_200_OK)
            data = {'username': 'testuser2'}
            response_user_put = self.client.put(user_url, data=data)
            self.assertEqual(response_user_put.status_code, status.HTTP_200_OK)
            self.assertIsInstance(response_user_put.data, dict)
            self.assertEqual(response_user_put.data.get('username'), data.get('username'))

    def test_users_options(self):
        url = reverse('api:user-list')
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)



class UsersAnonymousTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

    def test_users_view(self):
        url = reverse('api:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for user in response.data:
            user_url = user.get('url')
            response_user_get = self.client.get(user_url)
            self.assertEqual(response_user_get.status_code, status.HTTP_200_OK)

    def test_users_options(self):
        url = reverse('api:user-list')
        response = self.client.options(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
