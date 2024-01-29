from rest_framework import filters
from django.db.models import Q


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
        Фильтрует категории трат, позволяя пользователям получить общие категории и созданные самим пользователеме
    """
    def filter_queryset(self, request, queryset, view):
        filtered_queryset = queryset.filter(Q(user=request.user) | Q(is_custom=False))
        return filtered_queryset
