from rest_framework import filters


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """ Фильтр для получения записей бд, принадлежащих только этому пользователю """

    def filter_queryset(self, request, queryset, view):
        filtered_queryset = queryset.filter(user=request.user)
        return filtered_queryset
