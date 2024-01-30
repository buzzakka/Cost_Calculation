from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
import datetime

from .models import *


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'costs/main.html'
    login_url = reverse_lazy('users:login')

    def get_pie_chart_data(self) -> list:
        user = self.request.user
        current_date = datetime.date.today()
        graph_info = (Cost.objects.filter(user=user, date__month=current_date.month, date__year=current_date.year)
                      .values('category__name').annotate(Sum('value')))
        chart_data = [{'name': elem['category__name'], 'y': float(elem['value__sum'])} for elem in graph_info]
        return chart_data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pie_chart_data'] = self.get_pie_chart_data()
        print(context)
        return context


class CostsHistory(LoginRequiredMixin, ListView):
    model = Cost
    template_name = 'costs/costs_history.html'
    context_object_name = 'history_list'

    def get_queryset(self):
        return Cost.objects.filter(user=self.request.user).order_by('date')

    def get_costs_history_data(self):
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
                {'value': cost.value, 'category': cost.category, 'description': cost.description}
            )
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['costs_history'] = self.get_costs_history_data()
        return context
