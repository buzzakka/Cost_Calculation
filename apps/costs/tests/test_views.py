from django.contrib.auth import get_user_model
from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
from datetime import date

from apps.costs.models import CostCategory, Cost

User = get_user_model()


class ViewsTest(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.std_category = CostCategory.objects.create(name='std', is_custom=False)

        cls.user_1 = User.objects.create_user(username='user_1', email='u1@u.u')
        cls.u1_category = CostCategory.objects.create(name='u1', user=cls.user_1)
        cls.u1_cost_1 = Cost.objects.create(
            value=1, category=cls.u1_category, user=cls.user_1, date=date.today().isoformat(), description='descr 1')
        cls.u1_cost_2 = Cost.objects.create(
            value=2, category=cls.std_category, user=cls.user_1, date=date.today().isoformat(), description='descr 1')
        cls.u1_cost_3 = Cost.objects.create(
            value=3, category=cls.std_category, user=cls.user_1, date='2023-01-01', description='descr 3')

        cls.user_2 = User.objects.create_user(username='user_2', email='u2@u.u')
        cls.u2_category = CostCategory.objects.create(name='u2', user=cls.user_2)
        cls.u2_cost = Cost.objects.create(
            value=2, category=cls.u2_category, user=cls.user_2, date=date.today().isoformat())

        cls.guest_client = Client()
        cls.authorized_client_1 = Client()
        cls.authorized_client_1.force_login(cls.user_1)
        cls.authorized_client_2 = Client()
        cls.authorized_client_2.force_login(cls.user_2)

    def setUp(self):
        self.factory = RequestFactory()

    def test_views_correct_template(self):
        """ URL-адрес использует соответствующий шаблон """
        templates_url_names = {
            reverse('costs:main'): 'costs/main.html',
            reverse('costs:history'): 'costs/costs_history.html',
            reverse('costs:add_cost'): 'costs/add_cost.html',
            reverse('costs:update_cost', kwargs={'pk': self.u1_cost_1.id}): 'costs/update_cost.html',
            reverse('costs:delete_cost', kwargs={'pk': self.u1_cost_1.id}): 'costs/cost_confirm_delete.html',
            reverse('costs:categories_list'): 'costs/categories_list.html',
            reverse('costs:add_category'): 'costs/add_category.html',
            reverse('costs:delete_category', kwargs={'pk': self.u1_category.id}): 'costs/category_confirm_delete.html',
            reverse('costs:update_category', kwargs={'pk': self.u1_category.id}): 'costs/update_category.html',
        }

        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client_1.get(address)
                error_name = f'Ошибка: {address} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)

    def test_costs_main_show_correct_context(self):
        """ Шаблон main сформирован с правильным контекстом """
        response = self.authorized_client_1.get(reverse('costs:main'))
        correct_context: dict = {
            'title': 'Статистика',
            'pie_chart_data': [
                {'name': 'std', 'y': 2.0},
                {'name': 'u1', 'y': 1.0},
            ],
            'current_month_costs': [
                {'category__name': 'std', 'value__sum': 2},
                {'category__name': 'u1', 'value__sum': 1},
            ]
        }
        for param, value in correct_context.items():
            error_name = f'Ошибка в параметре {param}: ожидаемое значение {value}, полученное значение {correct_context[param]}'
            if param != 'current_month_costs':
                self.assertEquals(response.context[param], value, error_name)
            else:
                self.assertEquals(list(response.context[param]), value, error_name)

    def test_cost_history_show_correct_context(self):
        """ Шаблон cost_history сформирован с правильным контекстом """
        response = self.authorized_client_1.get(reverse('costs:history'))
        correct_context: dict = {
            'costs_history': {
                date.today().year: {
                    date.today().month: [
                        {'id': 1, 'value': 1, 'category': self.u1_category, 'description': 'descr 1',
                         'date': date.today()},
                        {'id': 2, 'value': 2, 'category': self.std_category, 'description': 'descr 1',
                         'date': date.today()},
                    ]
                },
                2023: {
                    1: [
                        {'id': 3, 'value': 3, 'category': self.std_category, 'description': 'descr 3',
                         'date': date(2023, 1, 1)}
                    ],
                }
            },
            'title': 'История затрат'
        }
        for param, value in correct_context.items():
            self.assertEquals(response.context[param], value)

    def test_categories_list_show_correct_context(self):
        """ Шаблон categories_list сформирован с правильным контекстом """
        response = self.authorized_client_1.get(reverse('costs:categories_list'))
        categories = CostCategory.objects.all().exclude(user=self.user_2)
        self.assertEquals(list(response.context['categories']), list(categories))
