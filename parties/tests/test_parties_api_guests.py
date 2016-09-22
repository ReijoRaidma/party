from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from parties.models import User, Party, Guest


class GuestsSuperuserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_add_guest(self):
        Party.objects.create(name='Test1', owner=self.user)
        Party.objects.create(name='Test2', owner=self.user)
        url = reverse('api:guest-list')
        party = self.client.get(reverse('api:party-list')).data[0].get('url')
        data = ({
            'name': 'testname',
            "birth_date": "2016-09-15",
            "party": party
        })
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('url', response.data)
        self.assertEqual(data.get('name'), response.data.get('name'))
        self.assertEqual(data.get('party'), response.data.get('party'))

    def test_edit_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        Party.objects.create(name='Test2', owner=self.user)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        guest = self.client.get(reverse('api:guest-list')).data[0]
        party2_url = self.client.get(reverse('api:party-list')).data[1].get('url')
        data = ({
            'name': 'changed name',
            "birth_date": "2000-09-15",
            "party": party2_url
        })
        response = self.client.put(guest.get('url'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertNotEqual(guest.get('name'), response.data.get('name'))
        self.assertEqual(response.data.get('name'), 'changed name')
        self.assertNotEqual(response.data.get('party'), guest.get('party'))
        self.assertEqual(response.data.get('party'), party2_url)

    def test_delete_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        guest = self.client.get(reverse('api:guest-list')).data[0]
        response = self.client.delete(guest.get('url'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GuestsUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_add_guest(self):
        Party.objects.create(name='Test1', owner=self.user)
        Party.objects.create(name='Test2', owner=self.user)
        url = reverse('api:guest-list')
        party = self.client.get(reverse('api:party-list')).data[0].get('url')
        data = ({
            'name': 'testname',
            "birth_date": "2016-09-15",
            "party": party
        })
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        self.assertIn('url', response.data)
        self.assertEqual(data.get('name'), response.data.get('name'))
        self.assertEqual(data.get('party'), response.data.get('party'))

    def test_edit_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        Party.objects.create(name='Test2', owner=self.user)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        guest = self.client.get(reverse('api:guest-list')).data[0]
        party2_url = self.client.get(reverse('api:party-list')).data[1].get('url')
        data = ({
            'name': 'changed name',
            "birth_date": "2000-09-15",
            "party": party2_url
        })
        response = self.client.put(guest.get('url'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertNotEqual(guest.get('name'), response.data.get('name'))
        self.assertEqual(response.data.get('name'), 'changed name')
        self.assertNotEqual(response.data.get('party'), guest.get('party'))
        self.assertEqual(response.data.get('party'), party2_url)

    def test_delete_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        guest = self.client.get(reverse('api:guest-list')).data[0]
        response = self.client.delete(guest.get('url'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class GuestsAnonymousUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_superuser(
            username='superuser',
            email='test@example.com',
            password='superpassword',
        )

    def setUp(self):
        party = Party.objects.create(name='Test1', owner=self.user, is_public=True)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=party, owner=self.user)
    def test_guest_list_view(self):
        url = reverse('api:guest-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0].get('is_public'), False)
        self.assertEqual(response.data[0].get('name'), 'name')

    def test_anonymous_guest_create(self):
        Party.objects.create(name='Test1', owner=self.user)
        party = self.client.get(reverse('api:party-list')).data[0].get('url')
        url = reverse('api:guest-list')
        data = ({
            'name': 'testname',
            "birth_date": "2016-09-15",
            "party": party
        })
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
