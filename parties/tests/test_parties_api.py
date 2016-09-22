from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from parties.models import User, Party


class PartiesSuperuserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_create_party(self):
        url = reverse('api:party-list')
        data = {
            'name': 'test party',
            'is_public': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('url', response.data)
        self.assertEqual(data.get('name'), response.data.get('name'))
        self.assertEqual(data.get('is_public'), response.data.get('is_public'))

    def test_search_party(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        party2 = Party.objects.create(name='Test2', owner=self.user)