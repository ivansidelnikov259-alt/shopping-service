"""
Модели приложения purchases.
"""
from django.db import models
from django.urls import reverse
from homepage.models import TimeStampedModel
from django.db.models import Case, When, Value, BooleanField


class Category(models.Model):
    """Категория товаров."""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
        db_table = "categories"

    def __str__(self):
        return self.name


class Store(models.Model):
    """Магазин."""
    name = models.CharField(
        max_length=150,
        verbose_name="Название магазина"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Адрес"
    )

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = ["name"]
        db_table = "stores"

    def __str__(self):
        return self.name


class Purchase(TimeStampedModel):
    """Покупка."""
    product_name = models.CharField(
        max_length=200,
        verbose_name="Название товара"
    )
    price = models.FloatField(
        verbose_name="Цена"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="purchases",
        verbose_name="Категория"
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchases",
        verbose_name="Магазин"
    )
    purchase_date = models.DateField(
        verbose_name="Дата покупки"
    )
    is_expensive = models.GeneratedField(
        expression=Case(
            When(price__gte=1000, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        ),
        output_field=BooleanField(),
        db_persist=True,
        verbose_name="Дорогая покупка",
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        ordering = ["-purchase_date"]
        db_table = "purchases"

    def __str__(self):
        return f"{self.product_name} - {self.price} руб."

    def get_absolute_url(self):
        return reverse("purchases:detail", kwargs={"purchase_id": self.pk})
