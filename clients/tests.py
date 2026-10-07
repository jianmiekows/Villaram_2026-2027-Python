from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/clients/'

    def test_user_crud_and_password_hashing(self):
        response = self.client.post(
            self.url,
            {
                'username': 'test-user',
                'email': 'test@example.com',
                'password': 'Strong-Passphrase-194',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)

        user = get_user_model().objects.get(username='test-user')
        self.assertTrue(user.check_password('Strong-Passphrase-194'))
        detail_url = f'{self.url}{user.pk}/'

        self.assertEqual(self.client.get(self.url).status_code, 403)
        admin = get_user_model().objects.create_user(
            username='api-admin',
            password='Admin-Strong-Passphrase-306',
            is_staff=True,
        )
        self.client.force_authenticate(user=admin)
        self.assertEqual(self.client.get(self.url).status_code, 200)
        self.assertEqual(self.client.get(detail_url).status_code, 200)

        response = self.client.patch(
            detail_url,
            {'password': 'Another-Strong-Passphrase-295'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password('Another-Strong-Passphrase-295'))

        self.assertEqual(self.client.delete(detail_url).status_code, 204)
        self.assertFalse(get_user_model().objects.filter(pk=user.pk).exists())
