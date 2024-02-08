from datetime import date

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from decimal import Decimal

from apps.costs.models import CostCategory, Cost


class CostCategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Создаётся 2 объекта категории: стандартный и пользовательский
        """
        cls.user = get_user_model().objects.create_user(username='user', email='user@mail.com', password='qpwoer!@#1')
        cls.standart_cost_category = CostCategory.objects.create(name='Standart Category', is_custom=False)
        cls.custom_cost_category = CostCategory.objects.create(name='user Category', is_custom=True, user=cls.user)

    def test_verbose_names(self):
        field_verboses = {
            'name': 'Название',
            'is_custom': 'Добавлена пользователем',
            'user': 'Пользователь'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.standart_cost_category._meta.get_field(field).verbose_name,
                    expected_value, error_name
                )

    def test_standart_category_1(self):
        """
        Параметры добавленной стандартной категории
        """
        self.assertEquals(self.standart_cost_category.name, 'Standart Category')
        self.assertEquals(self.standart_cost_category.is_custom, False)
        self.assertIsNone(self.standart_cost_category.user)

    def test_standart_category_2(self):
        """
        Создание новой стандартной категории с именем, которое есть у пользовательской категории
        """
        CostCategory.objects.create(name='user Category', is_custom=False)
        category = CostCategory.objects.get(name='user Category', is_custom=False, user=None)
        self.assertEquals(category.name, 'user Category')
        self.assertEquals(category.is_custom, False)
        self.assertIsNone(category.user)

    def test_standart_category_raise_error(self):
        """
        Возникновение ошибки при добавлении новой стандартной категории, которая уже существует в системе
        """
        category = CostCategory(name='Standart Category', is_custom=False)
        with self.assertRaisesMessage(ValidationError, 'Категория с таким названием уже существует'):
            category.clean()

    def test_user_category_1(self):
        """
        Параметры добавленной пользовательской категории
        """
        self.assertEquals(self.custom_cost_category.name, 'user Category')
        self.assertEquals(self.custom_cost_category.is_custom, True)
        self.assertEquals(self.custom_cost_category.user, self.user)

    def test_user_category_raise_error_1(self):
        """
        Вознекновение ошибки при добавлении новой пользовательской категории, которая уже существует у этого пользователя
        """
        category = CostCategory(name='user Category', is_custom=True, user=self.user)
        with self.assertRaisesMessage(ValidationError, 'Категория с таким названием уже существует'):
            category.clean()

    def test_user_category_raise_error_2(self):
        """
        Вознекновение ошибки при добавлении новой пользовательской категории, имя которой совпадает со стандартной категорией
        """
        category = CostCategory(name='Standart Category', is_custom=True, user=self.user)
        with self.assertRaisesMessage(ValidationError, 'Категория с таким названием уже существует'):
            category.clean()

    def test_category_str(self):
        """
        Проверка метода ___str___()
        """
        category = CostCategory.objects.get(name='Standart Category')
        self.assertEquals(category.__str__(), 'Standart Category')


class CostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Создается пользователь, категория и трата созданного пользователя с созданной категорией
        """
        cls.user = get_user_model().objects.create_user(username='user', email='user@mail.com', password='qpwoer!@#1')
        cls.standart_category = CostCategory.objects.create(name='Standard', is_custom=False)
        cls.custom_category = CostCategory.objects.create(name='Custom', user=cls.user)
        Cost.objects.create(value=1500.23, user=cls.user, category=cls.standart_category,
                            description='Описание затраты',
                            date='2023-10-10')

    def test_cost_with_standart_category_values(self):
        """
        Параметры добавленной в setUpTestData траты
        """
        cost = Cost.objects.filter(user=self.user).first()
        self.assertEquals(cost.value, Decimal('1500.23'))
        self.assertEquals(cost.user, self.user)
        self.assertEquals(cost.category, self.standart_category)
        self.assertEquals(cost.description, 'Описание затраты')
        self.assertEquals(cost.date, date(2023, 10, 10))

    def test_create_cost_with_own_category(self):
        """
        Созданиее траты со своей категорией
        """
        cost = Cost.objects.create(value=11, user=self.user, category=self.custom_category)
        self.assertEquals(cost.value, Decimal('11'))
        self.assertEquals(cost.user, self.user)
        self.assertEquals(cost.category, self.custom_category)

    # def test_cost_with_other_user_category_error(self):
    #     """
    #     Возникновение ошибки в том случае, когда пользователь пытается создать трату с категорией другого пользователя
    #     """
    #     user_2 = get_user_model().objects.create_user(username='user_2', email='user2@mail.com', password='qpwoer!@#1')
    #     user_2_cost_category = CostCategory.objects.create(name='Standard', user=user_2)
    #     cost = Cost.objects.create(value=10, user=self.user, category=user_2_cost_category)
    #     with self.assertRaisesMessage(ValidationError, 'Категория не найдена'):
    #         cost.clean()

    def test_cost_str(self):
        """
        Проверка метода ___str___()
        """
        cost = Cost.objects.get(value=1500.23)
        self.assertEquals(cost.__str__(), 'Пользователь: user, сумма: 1500.23, категория: Standard')
