from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse




class AuthTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        User.objects.create_user(username=self.username, password=self.password)

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('profile'))
        self.assertEqual(self.client.session['_auth_user_id'], str(User.objects.get(username=self.username).id))

    def test_login_protection(self):
        response = self.client.get(reverse('recipe:add_recipe'))
        self.assertRedirects(response, '/login/?next=/add/')

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('logout_success'))
        self.assertNotIn('_auth_user_id', self.client.session)

    