from django import forms
from .models import Purchase, Category, Store
from datetime import date  # Импортируем date для проверки

class PurchaseForm(forms.ModelForm):
    category_name = forms.CharField(
        label="Категория",
        required=True,
        widget=forms.TextInput(attrs={'list': 'category-list', 'class': 'form-control'})
    )
    store_name = forms.CharField(
        label="Магазин",
        required=False,
        widget=forms.TextInput(attrs={'list': 'store-list', 'class': 'form-control'})
    )

    class Meta:
        model = Purchase
        fields = ['product_name', 'price', 'purchase_date']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['category_name'].initial = self.instance.category.name
            if self.instance.store:
                self.fields['store_name'].initial = self.instance.store.name

    def clean_category_name(self):
        name = self.cleaned_data['category_name'].strip()
        if not name:
            raise forms.ValidationError("Введите название категории")
        return name

    def clean_store_name(self):
        return self.cleaned_data['store_name'].strip()

    # --- НОВАЯ ВАЛИДАЦИЯ ДАТЫ ---
    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('purchase_date')
        if purchase_date and purchase_date > date.today():
            raise forms.ValidationError("Дата покупки не может быть в будущем.")
        return purchase_date

    def save(self, commit=True):
        category_name = self.cleaned_data['category_name']
        category, _ = Category.objects.get_or_create(name=category_name)
        
        store_name = self.cleaned_data['store_name']
        store = None
        if store_name:
            store, _ = Store.objects.get_or_create(name=store_name, defaults={'address': ''})
        
        purchase = super().save(commit=False)
        purchase.category = category
        purchase.store = store
        if commit:
            purchase.save()
        return purchase


# Формы для создания категорий и магазинов
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
