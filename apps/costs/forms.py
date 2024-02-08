from django import forms
from django.db.models import Q
from .models import Cost, CostCategory
from apps.users.forms import AddPlaceholderFormMixin


class AddCostCategoryForm(forms.ModelForm, AddPlaceholderFormMixin):
    """ Форма добавления новой категории """

    class Meta:
        model = CostCategory
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        """
        На вход принимает именованный параметр user - текущий пользователь и добавляет в
        текущий экземпляр объекта формы
        """
        self.user = kwargs.pop('user')
        super(AddCostCategoryForm, self).__init__(*args, **kwargs)
        self.add_placeholder()


class AddCostForm(forms.ModelForm, AddPlaceholderFormMixin):
    """ Форма добавления новой траты """

    class Meta:
        model = Cost
        fields = ('value', 'category', 'description', 'date')

    def __init__(self, *args, **kwargs):
        """
        На вход принимает именованный параметр user - текущий пользователь и добавляет в текущий экземпляр объекта
        формы. Также в поле category добавляет только стандартные категории, и категории, созданные пользователем
        """
        self.user = kwargs.pop('user')
        super(AddCostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = CostCategory.objects.filter(
            Q(user=self.user) | Q(is_custom=False)
        )
        self.add_placeholder()
