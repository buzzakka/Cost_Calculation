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

    def clean_name(self):
        name = self.cleaned_data['name']
        if CostCategory.objects.filter(
                (Q(user=self.user) & Q(name=name)) | (Q(is_custom=False) & Q(name=name))).exists():
            raise forms.ValidationError("Такая категория уже существует")
        else:
            return name


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

