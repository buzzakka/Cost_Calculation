from django.contrib.auth.backends import ModelBackend, get_user_model
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

class CustomUserBackend(ModelBackend):
    """ Бэкенд для авторизации пользователей через username и email """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(Q(username=username) | Q(email__iexact=username))
        except user_model.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return user_model.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
