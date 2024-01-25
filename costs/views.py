from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = reverse_lazy('users:login')
