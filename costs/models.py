from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CostCategory(models.Model):
    """
        Модель, описывающая стандартную категорию затрат, общие для всех пользователей, создается админом
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    is_custom = models.BooleanField(default=True, verbose_name='Добавлена пользователем')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория затрат'
        verbose_name_plural = 'Категории затрат'


class Cost(models.Model):
    """
        Модель, описывающая конкретную затрату пользоватлея
    """
    value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Затраченная сумма')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(CostCategory, on_delete=models.CASCADE, verbose_name='Категория затраты')

    def __str__(self):
        return f'cost_id: {self.pk}, value: {self.value}'

    class Meta:
        verbose_name = 'Трата'
        verbose_name_plural = 'Затраты'
        ordering = ('user', 'category', 'value')
