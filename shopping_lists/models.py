"""
Модели приложения shopping_lists.
"""
from django.db import models


class ShoppingList(models.Model):
    """Список покупок."""
    name = models.CharField(
        max_length=200,
        verbose_name="Название списка"
    )
    created_at = models.DateField(
        verbose_name="Дата создания"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Завершён"
    )

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ["-created_at"]
        db_table = "shopping_lists"  # Привязка к таблице из ПР7

    def __str__(self):
        return self.name


class ShoppingListItem(models.Model):
    """Элемент списка покупок."""
    shopping_list = models.ForeignKey(
        ShoppingList,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Список покупок"
    )
    product_name = models.CharField(
        max_length=200,
        verbose_name="Название товара"
    )
    price = models.FloatField(
        verbose_name="Цена"
    )

    class Meta:
        verbose_name = "Элемент списка"
        verbose_name_plural = "Элементы списка"
        db_table = "shopping_list_items"  # Привязка к таблице из ПР7

    def __str__(self):
        return f"{self.product_name} ({self.price} руб.)"
    