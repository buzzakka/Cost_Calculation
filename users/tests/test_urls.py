from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


# TODO: Надо добавить проверку шаблона 'password-reset/<uidb64>/<token>/'
class UsersURLTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auth')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_urls_guest_client_with_OK_HTTP_Status(self):
        """ Доступ неавторизованного пользователя к страницам, к которым у него есть право доступа """
        pages: tuple = (
            '/users/login/',
            '/users/register/',
            '/users/password-reset/',
            '/users/password-reset/complete/',
            '/users/password-reset/done/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            error_message = f'Ошибка с доступом к странице {page}'
            self.assertEquals(response.status_code, HTTPStatus.OK, error_message)

    def test_urls_guest_client_to_login_required_pages(self):
        """ Доступ неавторизованного пользователя к страница с LoginRequired """
        pages: tuple = (
            '/users/change-password/',
        )
        for page in pages:
            target_page = f'/users/login/?next={page}'
            response = self.guest_client.get(page)
            self.assertRedirects(response, target_page)

    def test_urls_authorized_client_with_OK_HTTP_Status(self):
        """ Доступ авторизованного пользователя к страницам, к которым у него есть доступ """
        pages: tuple = (
            '/users/change-password/',
        )
        for page in pages:
            response = self.authorized_client.get(page)
            error_message = f'Ошибка с доступом к странице {page}'
            self.assertEquals(response.status_code, HTTPStatus.OK, error_message)

    def test_urls_authorized_client_to_unauthorized_pages(self):
        """
        Доступ авторизованного пользователя к странице, к которой есть доступ только у неавторизованных пользователей
        """
        pages: tuple = (
            '/users/login/',
            '/users/register/',
            '/users/password-reset/',
            '/users/password-reset/complete/',
            '/users/password-reset/done/',
        )
        for url in pages:
            target_page = '/costs/'
            response = self.authorized_client.get(url)
            self.assertRedirects(response, target_page)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_url_names: dict = {
            '/users/login/': 'users/login.html',
            '/users/register/': 'users/register.html',
            '/users/password-reset/': 'users/password_reset_form.html',
            '/users/password-reset/done/': 'users/password_reset_done.html',
            '/users/password-reset/complete/': 'users/password_reset_complete.html',
            '/users/change-password/': 'users/change_password.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = (self.guest_client.get(adress) if adress != '/users/change-password/'
                            else self.authorized_client.get(adress))
                error_name = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)

    def test_logout(self):
        """ Функция logout """
        response = self.authorized_client.post('/users/logout/')
        self.assertIsNone(response.context)
        self.assertRedirects(response, '/users/login/')
