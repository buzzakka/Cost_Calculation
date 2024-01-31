from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import Resolver404


class UsersObjectMixin(LoginRequiredMixin):
    """
    Миксин, который проверяет, относится ли данная категория к текущему пользователю
    """
    def is_users_object(self, request):
        object = self.get_object()
        return object.user == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.is_users_object(request):
            raise Resolver404('Объект не найден')
        return super().dispatch(request, *args, **kwargs)


class AddUserToNewObjectMixin(LoginRequiredMixin):
    """
    Миксин, который добавляет пользователя к новому объекту
    """
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
