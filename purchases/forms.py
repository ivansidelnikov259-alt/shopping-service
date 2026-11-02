from django import forms
from django.core.exceptions import ValidationError  
from datetime import date
from .models import Purchase, Category, Store

class PurchaseForm(forms.ModelForm):
    # Переопределяем поля как текстовые
    category_name = forms.CharField(
        label="Категория", 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Продукты'})
    )
    store_name = forms.CharField(
        label="Магазин", 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Магнит'})
    )

    class Meta:
        model = Purchase
        fields = ['product_name', 'price', 'purchase_date']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если редактируем, заполняем поля начальными значениями
        if self.instance and self.instance.pk:
            self.fields['category_name'].initial = self.instance.category.name
            self.fields['store_name'].initial = self.instance.store.name if self.instance.store else ""

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Ищем или создаём категорию
        cat_name = self.cleaned_data.get('category_name').strip()
        category, _ = Category.objects.get_or_create(name=cat_name)
        instance.category = category

        # Ищем или создаём магазин (если ввели)
        store_name = self.cleaned_data.get('store_name').strip()
        if store_name:
            store, _ = Store.objects.get_or_create(name=store_name)
            instance.store = store
        else:
            instance.store = None

        if commit:
            instance.save()
        return instance
    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('purchase_date')
        if purchase_date and purchase_date > date.today():
            raise ValidationError("Дата покупки не может быть в будущем.")
        return purchase_date


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
