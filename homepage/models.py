"""
Абстрактные модели предметной области.
"""
from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактная модель с датой создания и обновления."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        abstract = True
        