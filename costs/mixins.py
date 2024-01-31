from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import Resolver404


class UserCategoryMixin(LoginRequiredMixin):
    def is_users_category(self, request):
        object = self.get_object()
        return object.user == request.user

    def dispatch(self, request, *args, **kwargs):
        if not self.is_users_category(request):
            raise Resolver404('Данная категория затрат не найдена')
        return super().dispatch(request, *args, **kwargs)