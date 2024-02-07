from decimal import Decimal
from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.costs.models import CostCategory, Cost

User = get_user_model()


class CostCategoryFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', email='test@test.com')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.std_category = CostCategory.objects.create(name='std cat', is_custom=False)
        cls.users_category_1 = CostCategory.objects.create(name='user cat 1', user=cls.user)
        cls.users_category_2 = CostCategory.objects.create(name='user cat 2', user=cls.user)

        cls.user_2 = User.objects.create_user(username='user 2')
        cls.user_2_categoy = CostCategory.objects.create(name='user_2 cat', user=cls.user_2)

    def test_add_cost_category(self):
        """ Создание новой категории затрат """
        categories_count = CostCategory.objects.count()
        form_data = {'name': 'Test Category'}
        response = self.authorized_client.post(reverse('costs:add_category'), form_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        error_name_1 = 'Данные категорий не совпадают'
        self.assertTrue(CostCategory.objects.filter(name='Test Category', user=self.user).exists(), error_name_1)
        error_name_2 = 'Поcт не добавлен в базу данных'
        self.assertEquals(CostCategory.objects.count(), categories_count + 1, error_name_2)

    def test_add_existing_cost_category(self):
        """ Добавление уже существующей категории затрат """
        CostCategory.objects.create(name='Test', is_custom=False)
        categories_count = CostCategory.objects.count()
        form_data = {'name': 'Test'}

        response = self.authorized_client.post(reverse('costs:add_category'), form_data)
        self.assertEquals(categories_count, CostCategory.objects.count())
        self.assertContains(response, 'Категория с таким названием уже существует')

    def test_update_own_category(self):
        """ Обновление пользователем своей категории """
        objects_count = CostCategory.objects.all().count()
        form_data = {'name': 'Another test'}
        self.authorized_client.post(
            reverse('costs:update_category', kwargs={'pk': self.users_category_1.id}), form_data, follow=True)

        self.users_category_1.refresh_from_db()

        self.assertEquals(objects_count, CostCategory.objects.all().count())
        self.assertEquals(self.users_category_1.name, form_data['name'])
        self.assertEquals(self.users_category_1.user, self.user)

    def test_update_std_category(self):
        """ Попытка обновления пользователем стандартной категории """
        objects_count = CostCategory.objects.all().count()
        form_data = {'name': 'asd'}
        self.authorized_client.post(
            reverse('costs:update_category', kwargs={'pk': self.std_category.id}), form_data, follow=True)

        self.std_category.refresh_from_db()

        self.assertEquals(objects_count, CostCategory.objects.all().count())
        self.assertEquals(self.std_category.name, 'std cat')
        self.assertIsNone(self.std_category.user)

    # ПЕРЕДЕЛАТЬ МОДЕЛЬ КАТЕГОРИЙ
    def test_update_another_users_category(self):
        form_data = {'name': 'asd'}
        self.authorized_client.post(
            reverse('costs:update_category', kwargs={'pk': self.user_2_categoy.id}), form_data, follow=True)

        self.std_category.refresh_from_db()

        self.assertEquals(self.user_2_categoy.name, 'user_2 cat')
        # self.assertEquals(self.users_category_2.user, self.user_2)

    def test_delete_own_category(self):
        """ Удаление пользователем своей категории """
        objects_count = CostCategory.objects.all().count()
        self.authorized_client.post(
            reverse('costs:delete_category', kwargs={'pk': self.users_category_1.id}), follow=True)

        self.assertEquals(objects_count - 1, CostCategory.objects.all().count())

    def test_delete_standart_category(self):
        """ Попытка удаления пользователем стандартной категории """
        objects_count = CostCategory.objects.all().count()
        self.authorized_client.post(
            reverse('costs:delete_category', kwargs={'pk': self.std_category.id}), follow=True)

        self.assertEquals(objects_count, CostCategory.objects.all().count())

    def test_delete_other_users_category(self):
        """ Попытка удаления пользователем категории другого пользователя """
        objects_count = CostCategory.objects.all().count()
        self.authorized_client.post(
            reverse('costs:delete_category', kwargs={'pk': self.user_2_categoy.id}), follow=True)

        self.assertEquals(objects_count, CostCategory.objects.all().count())


class CostFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.standart_category = CostCategory.objects.create(name='Standart category', is_custom=False)

        cls.user = User.objects.create_user(username='user', email='test@test.com')
        cls.user_category = CostCategory.objects.create(name='User 1 category', user=cls.user)
        cls.user_cost = Cost.objects.create(value='1', category=cls.user_category, user=cls.user)

        cls.user_2 = User.objects.create_user(username='user2', email='test2@test.com')
        cls.user_2_category = CostCategory.objects.create(name='User 2 category', user=cls.user_2)
        cls.user_2_cost = Cost.objects.create(value='2', category=cls.user_2_category, user=cls.user_2)

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_add_cost_with_standart_category(self):
        """ Создание новой затраты со стандартной категорией """
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
        """ Создание новой затраты с кастомной категорией """
        costs_count = Cost.objects.count()
        form_data = {
            'value': 100,
            'category': self.user_category.id,
            'description': 'test description',
            'date': '2023-10-10'
        }
        response = self.authorized_client.post(reverse('costs:add_cost'), form_data, follow=True)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        error_name_1 = 'Данные затрат не совпадают'
        self.assertTrue(Cost.objects.filter(
            value=Decimal(100), category=self.user_category, user=self.user).exists(), error_name_1)
        error_name_2 = 'Поcт не добавлен в базу данных'
        self.assertEquals(Cost.objects.count(), costs_count + 1, error_name_2)

    def test_add_cost_with_other_user_category(self):
        count_1 = Cost.objects.all().count()
        user_2 = User.objects.create_user(username='n')
        u2_category = CostCategory.objects.create(name='qwe', user=user_2)
        form_data = {
            'value': 100,
            'category': u2_category.id,
            'description': 'test description',
            'date': '2023-10-10'
        }
        self.authorized_client.post(reverse('costs:add_cost'), form_data, follow=True)
        count_2 = Cost.objects.all().count()
        self.assertEquals(count_1, count_2)

    # def test_update_own_cost(self):
    #     """ Обновление пользователем своей траты """
    #     objects_count = Cost.objects.all().count()
    #     form_data = {
    #         'value': 13, 'category': self.standart_category, 'description': 'new description', 'date': '2024-02-02'}
    #     self.authorized_client.post(
    #         reverse('costs:update_cost', kwargs={'pk': self.user_cost.id}), form_data, follow=True)
    #
    #     self.user_cost.refresh_from_db()
    #
    #     self.assertEquals(objects_count, Cost.objects.all().count())
    #     for key, value in form_data.items():
    #         self.assertEquals(self.user_cost.__getattribute__(key), value)
    #     self.assertEquals(self.user_cost.user, self.user)

    def test_update_other_users_cost(self):
        """ Обновление пользователем траты другого пользователя """
        form_data = {
            'value': 13, 'category': self.user_category, 'description': 'new description', 'date': '2024-02-02'}
        self.authorized_client.post(
            reverse('costs:update_cost', kwargs={'pk': self.user_2_cost.id}), form_data, follow=True)

        self.user_2_cost.refresh_from_db()

        self.assertEquals(self.user_2_cost.user, self.user_2)
        self.assertEquals(self.user_2_cost.value, 2)
        self.assertEquals(self.user_2_cost.category, self.user_2_category)
        self.assertIsNone(self.user_2_cost.description)
