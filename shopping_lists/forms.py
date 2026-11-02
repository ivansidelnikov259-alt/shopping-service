from django import forms
from .models import ShoppingList, ShoppingListItem


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        # Оставляем только название. Статус будем менять отдельно.
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingListItem
        fields = ['product_name', 'price']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        