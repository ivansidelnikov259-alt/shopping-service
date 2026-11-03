"""
Модели приложения shopping_lists.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit


class ShoppingListQuerySet(models.QuerySet):
    """Кастомный QuerySet для фильтрации списков по статусу."""
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def archived(self):
        return self.filter(status=self.model.Status.ARCHIVED)


class ShoppingListManager(models.Manager.from_queryset(ShoppingListQuerySet)):
    """Менеджер для ShoppingList."""
    pass


class ShoppingList(models.Model):
    """Список покупок."""
    
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        COMPLETED = "completed", "Завершён"
        ARCHIVED = "archived", "В архиве"

    name = models.CharField(
        max_length=200,
        verbose_name="Название списка"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="URL-идентификатор"
    )
    created_at = models.DateField(
        verbose_name="Дата создания"
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус"
    )
    
    objects = ShoppingListManager()

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
        ordering = ["-created_at"]
        db_table = "shopping_lists"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Автоматическая генерация slug, если его нет
        if not self.slug:
            transliterated_name = translit(self.name, 'ru', reversed=True)
            base_slug = slugify(transliterated_name) or "list"
            
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Возвращает URL подробной страницы списка."""
        return reverse("shopping_lists:detail", kwargs={"list_id": self.pk})


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
        db_table = "shopping_list_items"

    def __str__(self):
        return f"{self.product_name} ({self.price} руб.)"
