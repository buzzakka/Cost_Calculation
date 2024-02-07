from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField


class CustomUser(AbstractUser):
    """
    Переопределенная модель пользователя
    Добавлено фото пользователя и поле email сделано обязательным
    """
    image = ImageField(upload_to='', blank=True)
    email = models.EmailField(verbose_name='E-mail', unique=True, max_length=244)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
