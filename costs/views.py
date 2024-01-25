from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.shortcuts import render

from .models import *


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = reverse_lazy('users:login')


class GraphView(LoginRequiredMixin, TemplateView):
    template_name = 'graph.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        graph_info = Cost.objects.filter(user=user).values('category__name').annotate(Sum('value'))
        chart_data = [{'name': elem['category__name'], 'y': float(elem['value__sum'])} for elem in graph_info]
        print(chart_data)
        return render(request, 'costs/graph.html', {'chart_data': chart_data})

