from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountViewTests(TestCase):
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вход')

    def test_register_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'new_user',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
        )

        self.assertRedirects(response, reverse('article_list'))
        self.assertTrue(User.objects.filter(username='new_user').exists())
        self.assertIn('_auth_user_id', self.client.session)
