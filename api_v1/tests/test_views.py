from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from api_v1.views import StandartCategoriesAPIView, CustomCategoriesAPIViewSet, CostsAPIViewSet
from costs.models import Cost, CostCategory

User = get_user_model()


class StandartCategoriesAPIViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='password')
        cls.client = APIClient()
        response = cls.client.post(reverse('api_v1:login'), {'username': 'user', 'password': 'password'})
        token = response.data['auth_token']
        cls.headers = {'Authorization': f'Token {token}'}

        cls.custom_category = CostCategory.objects.create(name='Custom Category', user=cls.user)
        cls.standart_category = CostCategory.objects.create(name='Standard Category', is_custom=False)

    def test_get_all_standart_categories(self):
        url = reverse('api_v1:common_categories')
        response = self.client.get(url, headers=self.headers)
        print(response.data[0] == self.standart_category)
        print(response.data[0])

