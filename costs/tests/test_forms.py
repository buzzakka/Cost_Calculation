from decimal import Decimal
from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from costs.forms import AddCostCategoryForm, AddCostForm
from costs.models import CostCategory, Cost

User = get_user_model()

class AddCostCategoryFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='auth', email='test@test.com')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_add_cost_category(self):
        """
        Создание новой категории затрат
        """
        categories_count = CostCategory.objects.count()
        form_data = {'name': 'Test Category'}
        response = self.authorized_client.post(reverse('costs:add_category'), form_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        error_name_1 = 'Данные категорий не совпадают'
        self.assertTrue(CostCategory.objects.filter(name='Test Category', user=self.user).exists(), error_name_1)
        error_name_2 = 'Поcт не добавлен в базу данных'
        self.assertEquals(CostCategory.objects.count(), categories_count + 1, error_name_2)

    def test_add_existing_cost_category(self):
        """
        Добавление уже существующей категории затрат
        """
        CostCategory.objects.create(name='Test', is_custom=False)
        categories_count = CostCategory.objects.count()
        form_data = {'name': 'Test'}

        response = self.authorized_client.post(reverse('costs:add_category'), form_data)
        self.assertEquals(categories_count, CostCategory.objects.count())
        self.assertContains(response, 'Категория с таким названием уже существует')


class AddCostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='auth', email='test@test.com')
        cls.standart_category = CostCategory.objects.create(name='Standart category', is_custom=False)
        cls.custom_category = CostCategory.objects.create(name='Custom category', is_custom=False, user=cls.user)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_add_cost_with_standart_category(self):
        """
        Создание новой затраты
        """
        costs_count = Cost.objects.count()
        form_data = {
            'value': 100,
            'category': self.standart_category.id,
            'description': 'test description',
            'date': '2023-10-10'
        }
        response = self.authorized_client.post(reverse('costs:add_cost'), form_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        error_name_1 = 'Данные затрат не совпадают'
        self.assertTrue(Cost.objects.filter(
            value=Decimal(100), category=self.standart_category, user=self.user).exists(), error_name_1)
        error_name_2 = 'Поcт не добавлен в базу данных'
        self.assertEquals(Cost.objects.count(), costs_count + 1, error_name_2)

    def test_add_cost_with_custom_category(self):
        """
        Создание новой затраты
        """
        costs_count = Cost.objects.count()
        form_data = {
            'value': 100,
            'category': self.custom_category.id,
            'description': 'test description',
            'date': '2023-10-10'
        }
        response = self.authorized_client.post(reverse('costs:add_cost'), form_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        error_name_1 = 'Данные затрат не совпадают'
        self.assertTrue(Cost.objects.filter(
            value=Decimal(100), category=self.custom_category, user=self.user).exists(), error_name_1)
        error_name_2 = 'Поcт не добавлен в базу данных'
        self.assertEquals(Cost.self.objects.count(), costs_count + 1, error_name_2)
