from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from costs.models import Cost, CostCategory
from http import HTTPStatus as status

User = get_user_model()


class CustomAPITestCase(APITestCase):
    """
    Класс с инициализацией стандартных объектов в setUpTestData
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')
        cls.client = APIClient()
        response = cls.client.post(reverse('api_v1:login'), {'username': 'user', 'password': 'password'})
        token = response.data['auth_token']
        cls.headers = {'Authorization': f'Token {token}'}

        cls.custom_category_1 = CostCategory.objects.create(name='Custom Category 1', user=cls.user)
        cls.custom_category_2 = CostCategory.objects.create(name='Custom Category 2', user=cls.user)
        cls.standart_category_1 = CostCategory.objects.create(name='Standard Category 1', is_custom=False)
        cls.standart_category_2 = CostCategory.objects.create(name='Standard Category 2', is_custom=False)

        cls.user_2 = User.objects.create_user(username='user2', email='t@t.t')
        cls.u2_custom_category = CostCategory.objects.create(name='Custom Category User 2', user=cls.user_2)


class CommonCategoriesTest(CustomAPITestCase):
    """ Тестирование стандартых эндпоинтов стандартных категорий """
    def test_get_all_standart_categories(self):
        """ Получение всех стандартных категорий """
        url = reverse('api_v1:common_categories-list')
        result = [{'id': 3, 'name': 'Standard Category 1'}, {'id': 4, 'name': 'Standard Category 2'}]
        response = self.client.get(url, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertEqual(response.data, result)

    def test_get_filtred_standart_categories(self):
        """ Получение части стандартных категорий """
        url = reverse('api_v1:common_categories-list')
        result = [{'id': 4, 'name': 'Standard Category 2'}]
        response = self.client.get(url, {'name': 'Standard Category 2'}, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertEqual(response.data, result)

    def test_get_standart_category_detail(self):
        """ Получение информации о стандартной категории """
        url = reverse('api_v1:common_categories-detail', kwargs={'pk': 3})
        result = {'id': 3, 'name': 'Standard Category 1'}
        response = self.client.get(url,  headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertEqual(response.data, result)

    def test_get_standart_category_with_incorrect_id(self):
        """ Попытка получения стандартной категории по id кастомной категории """
        url = reverse('api_v1:common_categories-detail', kwargs={'pk': 2})
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.NOT_FOUND)


    def test_get_standart_categories_without_authorization(self):
        """ Попытка получения стандартных категорий неавторизованного пользователя """
        url = reverse('api_v1:common_categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.UNAUTHORIZED)


class CustomCategoriesTest(CustomAPITestCase):
    """ Тестирование эндпоинтов кастомных категорий """
    def test_get_all_custom_categories_list(self):
        """ Получение всех кастомных категорий пользователь user """
        url = reverse('api_v1:custom_categories-list')
        result = [{'id': 1, 'name': 'Custom Category 1'}, {'id': 2, 'name': 'Custom Category 2'}]
        response = self.client.get(url, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertEqual(response.data, result)

    def test_get_filtred_custom_categories_list(self):
        """ Получение части кастомных категорий пользователь user """
        url = reverse('api_v1:custom_categories-list')
        result = [{'id': 1, 'name': 'Custom Category 1'}]
        response = self.client.get(url, {'id': 1}, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertEqual(response.data, result)

    def test_get_custom_categories_list_without_authorization(self):
        """ Попытка получения кастомных категорий неавторизованного пользователя """
        url = reverse('api_v1:custom_categories-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.UNAUTHORIZED)

    def test_get_custom_category_details(self):
        """ Получение деталей касомной категории """
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 1})
        data = {'id': 1, 'name': 'Custom Category 1'}
        response = self.client.get(url, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertEqual(response.data, data)

    def test_get_custom_category_details_with_incorrect_id(self):
        """ Получение деталей кастомной категории по id стандартной категории по методы get custom_categories """
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 3})
        response = self.client.get(url, headers=self.headers)
        self.assertEquals(response.status_code, status.NOT_FOUND)

    def test_get_custom_category_details_without_authorization(self):
        """ Получение деталей кастомной категории без авторизации """
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 2})
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.UNAUTHORIZED)

    def test_post_custom_category(self):
        """ Создание новой кастомной категории """
        data = {'name': 'Custom Category 3'}
        url = reverse('api_v1:custom_categories-list')
        response = self.client.post(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.CREATED)
        self.assertTrue(CostCategory.objects.filter(name='Custom Category 3', user=self.user).exists())

    def test_post_custom_category_without_authorization(self):
        """ Попытка создания новой кастомной категории неавторизованным пользователе """
        data = {'name': 'Custom Category 3'}
        url = reverse('api_v1:custom_categories-list')
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.UNAUTHORIZED)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 3', user=self.user).exists())

    def test_put_custom_category(self):
        """ Изменение кастомной категории через put """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 2})
        response = self.client.put(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertTrue(CostCategory.objects.filter(name='Custom Category 2_1', user=self.user).exists())
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2', user=self.user).exists())

    def test_put_standart_category_with_user_error(self):
        """ Попытка изменения стандартной категории через метод put эндпоинта custom-categories """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 3})
        response = self.client.put(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.NOT_FOUND)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2_1').exists())

    def test_put_another_users_custom_categroy_error(self):
        """ Попытка изменения кастомной категории другого пользователя """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 5})
        response = self.client.put(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.NOT_FOUND)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2_1').exists())

    def test_put_custom_category_without_authorization(self):
        """ Попытка изменения кастомной категории неавторизованным пользователем """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 2})
        response = self.client.put(url, data=data)
        self.assertEquals(response.status_code, status.UNAUTHORIZED)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2_1').exists())

    def test_patch_custom_category(self):
        """ Изменение кастомной категории через patch """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 2})
        response = self.client.patch(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.OK)
        self.assertTrue(CostCategory.objects.filter(name='Custom Category 2_1', user=self.user).exists())
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2', user=self.user).exists())

    def test_patch_standart_category_with_user_error(self):
        """ Попытка изменения стандартной категории через метод patch эндпоинта custom-categories """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 3})
        response = self.client.patch(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.NOT_FOUND)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2_1').exists())

    def test_patch_another_users_custom_categroy_error(self):
        """ Попытка изменения кастомной категории другого пользователя """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 5})
        response = self.client.patch(url, data=data, headers=self.headers)
        self.assertEquals(response.status_code, status.NOT_FOUND)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2_1').exists())

    def test_patch_custom_category_without_authorization(self):
        """ Попытка изменения кастомной категории неавторизованным пользователем """
        data = {'name': 'Custom Category 2_1'}
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 2})
        response = self.client.patch(url, data=data)
        self.assertEquals(response.status_code, status.UNAUTHORIZED)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 2_1').exists())

    def test_delete_custom_category(self):
        """ Удаление пользовательской категории """
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 1})
        self.assertTrue(CostCategory.objects.filter(name='Custom Category 1').exists())
        response = self.client.delete(url, headers=self.headers)
        self.assertEquals(response.status_code, status.NO_CONTENT)
        self.assertFalse(CostCategory.objects.filter(name='Custom Category 1').exists())

    def test_delete_another_users_custom_category(self):
        """ Удаление пользовательской категории другого пользователя """
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 5})
        self.assertTrue(CostCategory.objects.filter(id=5, name='Custom Category User 2').exists())
        response = self.client.delete(url, headers=self.headers)
        self.assertEquals(response.status_code, status.NOT_FOUND)
        self.assertTrue(CostCategory.objects.filter(id=5, name='Custom Category User 2').exists())

    def test_delete_custom_category_without_authorization(self):
        """ Попытка удаления стандартной категории через метод delete custom_categories  """
        url = reverse('api_v1:custom_categories-detail', kwargs={'pk': 1})
        self.assertTrue(CostCategory.objects.filter(id=1, name='Custom Category 1').exists())
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.UNAUTHORIZED)
        self.assertTrue(CostCategory.objects.filter(id=1, name='Custom Category 1').exists())
