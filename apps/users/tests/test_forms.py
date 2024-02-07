from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus

User = get_user_model()


class UserFormsTest(TestCase):
    """ Тестирование формы регистрации пользователя """
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = Client()

    def test_user_register_form(self):
        """ Проверка формы регистрации пользователя """
        self.assertFalse(User.objects.filter(username='user', email='user@mail.ru').exists())
        form_data = {
            'username': 'user',
            'email': 'user@mail.ru',
            'password1': 'useruser',
            'password2': 'useruser'
        }
        response = self.guest_client.post(reverse('users:register'), data=form_data)
        self.assertTrue(User.objects.filter(username=form_data['username'], email=form_data['email']).exists())
        self.assertRedirects(response, reverse('users:login'))

    def test_user_login_form_with_username(self):
        """ Проверка авторизацию пользователя через username """
        User.objects.create_user(username='user', email='user@mail.ru', password='useruser')
        form_data = {
            'username': 'user',
            'password': 'useruser'
        }
        response = self.guest_client.post(reverse('users:login'), data=form_data)
        self.assertRedirects(response, reverse('costs:main'))

        response_2 = self.guest_client.get(reverse('costs:main'))
        self.assertEquals(response_2.status_code, HTTPStatus.OK)

    def test_user_login_form_with_email(self):
        """ Проверка авторизацию пользователя через email """
        User.objects.create_user(username='user', email='user@mail.ru', password='useruser')
        form_data = {
            'username': 'user@mail.ru',
            'password': 'useruser'
        }
        response = self.guest_client.post(reverse('users:login'), data=form_data)
        self.assertRedirects(response, reverse('costs:main'))

        response_2 = self.guest_client.get(reverse('costs:main'))
        self.assertEquals(response_2.status_code, HTTPStatus.OK)
