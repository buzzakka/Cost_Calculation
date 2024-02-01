from django import forms
from django.db.models import Q
from .models import Cost, CostCategory


class AddCostCategoryForm(forms.ModelForm):
    class Meta:
        model = CostCategory
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddCostCategoryForm, self).__init__(*args, **kwargs)


class AddCostForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ('value', 'category', 'description', 'date')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AddCostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = CostCategory.objects.filter(
            Q(user=self.user) | Q(is_custom=False)
        )
