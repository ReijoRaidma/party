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
        party = Party.objects.create(name='Test1', owner=self.user)
        url = reverse('api:guest-list')
        party = reverse('api:party-detail', kwargs={'pk': party.id})
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
        self.assertIn(party, response.data.get('party'))

    def test_edit_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        party2 = Party.objects.create(name='Test2', owner=self.user)
        guest = Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        party2_url = reverse('api:party-detail', kwargs={'pk': party2.id})
        guest_url = reverse('api:guest-detail', kwargs={'pk': guest.id})
        data = ({
            'name': 'changed name',
            "birth_date": "2000-09-15",
            "party": party2_url,
        })
        response = self.client.put(guest_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('name'), data.get('name'))
        self.assertIn(party2_url, response.data.get('party'))

    def test_delete_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        guest = Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        guest_url = reverse('api:guest-detail', kwargs={'pk': guest.id})
        response = self.client.delete(guest_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GuestsUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test4321',
        )

        cls.anotheruser = User.objects.create_user(
            username='testuser1',
            email='test@example.com',
            password='test4321',
        )

    def setUp(self):
        self.client.force_authenticate(self.user)

    def test_user_get_guest_list(self):
        private_party = Party.objects.create(name='Test1', owner=self.anotheruser, is_public=False)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=private_party, owner=self.anotheruser)
        public_party = Party.objects.create(name='Test1', owner=self.anotheruser, is_public=True)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=public_party, owner=self.anotheruser)
        url = reverse('api:guest-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsInstance(response.data, list)

    def test_add_guest(self):
        party = Party.objects.create(name='Test1', owner=self.user)
        url = reverse('api:guest-list')
        party = reverse('api:party-detail', kwargs={'pk': party.id})
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
        self.assertIn(party, response.data.get('party'))

    def test_edit_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        party2 = Party.objects.create(name='Test2', owner=self.user)
        guest = Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        party2_url = reverse('api:party-detail', kwargs={'pk': party2.id})
        guest_url = reverse('api:guest-detail', kwargs={'pk': guest.id})
        data = ({
            'name': 'changed name',
            "birth_date": "2000-09-15",
            "party": party2_url,
        })
        response = self.client.put(guest_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data.get('name'), data.get('name'))
        self.assertIn(party2_url, response.data.get('party'))

    def test_delete_guest(self):
        party1 = Party.objects.create(name='Test1', owner=self.user)
        guest = Guest.objects.create(name='name', birth_date="2016-09-15", party=party1, owner=self.user)
        guest_url = reverse('api:guest-detail', kwargs={'pk': guest.id})
        response = self.client.delete(guest_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class GuestsAnonymousUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username='superuser',
            email='test@example.com',
            password='superpassword',
        )
        party = Party.objects.create(name='Test1', owner=cls.user, is_public=True)
        Guest.objects.create(name='name', birth_date="2016-09-15", party=party, owner=cls.user)

    def test_get_guest_list(self):
        url = reverse('api:guest-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_anonymous_guest_create(self):
        party = Party.objects.create(name='Test2', owner=self.user)
        party_url = reverse('api:party-detail', kwargs={'pk': party.id})
        url = reverse('api:guest-list')
        data = ({
            'name': 'testname',
            "birth_date": "2016-09-15",
            "party": party_url
        })
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
