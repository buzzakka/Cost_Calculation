from http import HTTPStatus
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from costs.models import Cost, CostCategory

User = get_user_model()


class CostsURLTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='auth')
        cls.category = CostCategory.objects.create(name="Test", user=cls.user)
        cls.cost = Cost.objects.create(value=10, category=cls.category, user=cls.user)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_guest_client_with_redirect(self):
        """Доступ неавторизованного пользователя с редиректом на LOGIN_URL"""
        pages: tuple = (
            '/costs/',
            '/costs/history/',
            '/costs/add-cost/',
            '/categories/',
            '/categories/add-category/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            expected_url = f'/users/login/?next={page}'
            self.assertRedirects(response, expected_url)

    def test_urls_guest_client_with_NOT_FOUND_HTTP_Status(self):
        """
        Доступ неавторизованного пользователя к старницам, к которым у него нет доступа,статус кода должен быть 404
        """
        pages: tuple = (
            f'/costs/update-cost/{self.cost.id}/',
            f'/costs/delete-cost/{self.cost.id}/',
            f'/categories/update-category/{self.category.id}/',
            f'/categories/delete-category/{self.category.id}/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_authorized_client_with_OK_HTTP_Status(self):
        """
        Доступ авторизованного пользователя к старницам, к которым у него есть доступ, статус кода должен быть 200
        """
        pages: tuple = (
            '/costs/',
            '/costs/history/',
            '/costs/add-cost/',
            f'/costs/update-cost/{self.cost.id}/',
            f'/costs/delete-cost/{self.cost.id}/',

            '/categories/',
            '/categories/add-category/',
            f'/categories/update-category/{self.category.pk}/',
            f'/categories/delete-category/{self.category.pk}/',
        )
        for page in pages:
            response = self.authorized_client.get(page)
            error_message = f'Ошибка с доступом к странице {page}'
            self.assertEquals(response.status_code, HTTPStatus.OK, error_message)

    def test_urls_authorized_client_with_NOT_FOUND_HTTP_Status(self):
        """
        Доступ авторизаванного пользователя к существующим страницам, к которым у него нет доступа
        Проверяется на основе доступа к редактированию/удалению стандартной категории, а также категории и
        затраты, созданными другим пользователем
        """
        standart_category = CostCategory.objects.create(name='standart', is_custom=False)

        user_2 = User.objects.create_user(username='user_2', email='q@q.q')
        category = CostCategory.objects.create(name='c2', user=user_2)
        cost = Cost.objects.create(value=1, category=category, user=user_2)

        pages: tuple = (
            f'/categories/update-category/{standart_category.pk}/',
            f'/categories/delete-category/{standart_category.pk}/',

            f'/costs/update-cost/{cost.id}/',
            f'/costs/delete-cost/{cost.id}/',
            f'/categories/update-category/{category.pk}/',
            f'/categories/delete-category/{category.pk}/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            self.assertEquals(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_url_names: dict = {
            '/costs/': 'costs/main.html',
            '/costs/history/': 'costs/costs_history.html',
            '/costs/add-cost/': 'costs/add_cost.html',
            f'/costs/update-cost/{self.cost.id}/': 'costs/update_cost.html',
            f'/costs/delete-cost/{self.cost.id}/': 'costs/cost_confirm_delete.html',

            '/categories/': 'costs/categories_list.html',
            '/categories/add-category/': 'costs/add_category.html',
            f'/categories/update-category/{self.category.pk}/': 'costs/update_category.html',
            f'/categories/delete-category/{self.category.pk}/': 'costs/category_confirm_delete.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)
