from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy, Resolver404
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, DeleteView
import datetime

from .models import *
from .forms import *


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'costs/main.html'
    login_url = reverse_lazy('users:login')

    def get_pie_chart_data(self) -> list:
        """
        Возвращает информацию для построения круговой диаграммы
        """
        graph_info = self.get_current_month_costs()
        chart_data = [{'name': elem['category__name'], 'y': float(elem['value__sum'])} for elem in graph_info]
        return chart_data

    def get_current_month_costs(self):
        """
        Возвращает список трат пользователя за текущий месяц, отсортированный по дате
        """
        user = self.request.user
        current_date = datetime.date.today()
        current_month_costs = (Cost.objects
                               .filter(user=user, date__month=current_date.month, date__year=current_date.year)
                               .values('category__name').annotate(Sum('value'))).order_by('date')
        return current_month_costs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_month_costs'] = self.get_current_month_costs()
        context['pie_chart_data'] = self.get_pie_chart_data()
        return context


class CostsHistory(LoginRequiredMixin, ListView):
    model = Cost
    template_name = 'costs/costs_history.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        return Cost.objects.filter(user=self.request.user).order_by('-date')

    def get_costs_history_data(self):
        """
        Вовращет словарь трат пользователя в формате
        {
            year1: {
                month1: [{'value1': value1, 'category1': category1, 'description1': description1}, ...],
                month2: ...,
                ...
            }
            year2: ...,
            ...
        }
        """
        queryset = self.get_queryset()
        year: int | None = None
        month: int | None = None
        data: dict = {}
        for cost in queryset:
            if cost.date.year != year:
                year = cost.date.year
                data[year] = {}
            if cost.date.month != month:
                month = cost.date.month
                data[year][month] = []
            data[year][month].append(
                {'value': cost.value, 'category': cost.category, 'description': cost.description, 'date': cost.date}
            )
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costs_history'] = self.get_costs_history_data()
        return context


class AddCategoryView(LoginRequiredMixin, CreateView):
    model = CostCategory
    form_class = AddCostCategoryForm
    template_name = 'costs/add_category.html'
    success_url = reverse_lazy('costs:add_category')

    def get_form_kwargs(self):
        kwargs = super(AddCategoryView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddCategoryView, self).form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = CostCategory
    template_name = 'costs/category_confirm_delete.html'
    success_url = reverse_lazy('costs:main')

    def is_users_category(self, request):
        object = self.get_object()
        return object.user == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.is_users_category(request):
            raise Resolver404('Данная категория затрат не найдена')
        return super(CategoryDeleteView, self).dispatch(request, *args, **kwargs)
