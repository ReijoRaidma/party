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
        url = reverse('api:party-list')
        Party.objects.create(name='Test1', owner=self.user)
        Party.objects.create(name='Test2', owner=self.user)
        params = {
            'search': 'Test1'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), params.get('search'))
        self.assertIn('url', response.data[0])

    def test_edit_party(self):
        Party.objects.create(name='Test1', owner=self.user)
        url = self.client.get(reverse('api:party-list')).data[0].get('url')
        data = {
            'name': 'Test1 after edit',
            'is_public': False
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('name'), data.get('name'))
        self.assertEqual(response.data.get('is_public'), data.get('is_public'))

    def test_delete_party(self):
        Party.objects.create(name='Test1', owner=self.user)
        url = self.client.get(reverse('api:party-list')).data[0].get('url')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PartiesUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )
        cls.superuser = User.objects.create_superuser(
            username='superuser',
            email='test@example.com',
            password='superpassword',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_view_party(self):
        Party.objects.create(name='Superuser not public party', owner=self.superuser, is_public=False)
        Party.objects.create(name='Testuser public party', owner=self.user, is_public=True)
        Party.objects.create(name='Testuser not public party', owner=self.user, is_public=False)
        url = reverse('api:party-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        for party in response.data:
            self.assertIn(party.get('name'), ['Testuser public party', 'Testuser not public party'])
        self.assertIsInstance(response.data, list)
        for party in response.data:
            self.assertNotEqual(party.get('name'), 'Superuser not public party')

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

    def test_search_user_party(self):
        url = reverse('api:party-list')
        Party.objects.create(name='Test1', owner=self.user)
        Party.objects.create(name='Test2', owner=self.user)
        Party.objects.create(name='Test3', owner=self.superuser, is_public=False)

        params = {
            'search': 'Test1'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), params.get('search'))
        self.assertIn('url', response.data[0])

    def test_search_public_party(self):
        url = reverse('api:party-list')
        Party.objects.create(name='Test1', owner=self.superuser, is_public=False)
        Party.objects.create(name='Test2', owner=self.superuser, is_public=True)
        params = {
            'search': 'Test'
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('name'), 'Test2')

    def test_edit_party(self):
        Party.objects.create(name='Test1', owner=self.user)
        url = self.client.get(reverse('api:party-list')).data[0].get('url')
        data = {
            'name': 'Test1 after edit',
            'is_public': False
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('name'), data.get('name'))
        self.assertEqual(response.data.get('is_public'), data.get('is_public'))

    def test_delete_party(self):
        Party.objects.create(name='Test1', owner=self.user)
        url = self.client.get(reverse('api:party-list')).data[0].get('url')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PartiesAnonymousUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_superuser(
            username='superuser',
            email='test@example.com',
            password='superpassword',
        )

    def setUp(self):
        Party.objects.create(name='Test1', owner=self.user, is_public=True)
        Party.objects.create(name='Test1', owner=self.user, is_public=False)

    def test_party_list_view(self):
        url = reverse('api:party-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0].get('is_public'), False)
        self.assertEqual(response.data[0].get('name'), 'Test1')

    def test_anonymous_party_create(self):
        url = reverse('api:party-list')
        data = {
            'name': 'test party',
            'is_public': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

