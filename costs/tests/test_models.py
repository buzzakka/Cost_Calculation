from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from costs.models import CostCategory, Cost


class CostCategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Создаётся 2 объекта категории: стандартный и пользовательский
        """
        cls.user_1 = get_user_model().objects.create_user(
            username='user_1', email='user1@mail.com', password='qpwoer!@#1')
        CostCategory.objects.create(name='Standart Category', is_custom=False)
        CostCategory.objects.create(name='User_1 Category', is_custom=True, user=cls.user_1)

    def test_standart_category_1(self):
        """
        Параметры добавленной стандартной категории
        """
        category = CostCategory.objects.get(name='Standart Category')
        self.assertEquals(category.name, 'Standart Category')
        self.assertEquals(category.is_custom, False)
        self.assertIsNone(category.user)

    def test_standart_category_2(self):
        """
        Создание новой стандартной категории с именем, которое есть у пользовательской категории
        """
        CostCategory.objects.create(name='User_1 Category', is_custom=False)
        category = CostCategory.objects.get(name='User_1 Category', is_custom=False, user=None)
        self.assertEquals(category.name, 'User_1 Category')
        self.assertEquals(category.is_custom, False)
        self.assertIsNone(category.user)

    def test_standart_category_raise_error(self):
        """
        Возникновение ошибки при добавлении новой стандартной категории,
        которая уже существует в системе
        """
        category = CostCategory(name='Standart Category', is_custom=False)
        with self.assertRaisesMessage(ValidationError, 'Категория с таким названием уже существует'):
            category.clean()
            category.save()

    def test_user_category_1(self):
        """
        Параметры добавленной пользовательской категории
        """
        category = CostCategory.objects.get(name='User_1 Category')
        self.assertEquals(category.name, 'User_1 Category')
        self.assertEquals(category.is_custom, True)
        self.assertEquals(category.user, self.user_1)

    def test_user_category_raise_error_1(self):
        """
        Вознекновение ошибки при добавлении новой пользовательской категории,
        которая уже существует у этого пользователя
        """
        category = CostCategory(name='User_1 Category', is_custom=True, user=self.user_1)
        with self.assertRaisesMessage(ValidationError, 'Категория с таким названием уже существует'):
            category.clean()
            category.save()

    def test_user_category_raise_error_2(self):
        """
        Вознекновение ошибки при добавлении новой пользовательской категории,
        имя которой совпадает со стандартной категорией
        """
        category = CostCategory(name='Standart Category', is_custom=True, user=self.user_1)
        with self.assertRaisesMessage(ValidationError, 'Категория с таким названием уже существует'):
            category.clean()
            category.save()

    def test_category_str(self):
        """
        Проверка метода ___str___()
        """
        category = CostCategory.objects.get(name='Standart Category')
        self.assertEquals(category.__str__(), 'Standart Category')
