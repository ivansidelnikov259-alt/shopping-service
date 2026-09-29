"""
Маршруты приложения purchases.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.purchases, name="purchases"),
    path("<int:purchase_id>/", views.purchase_detail, name="purchase_detail"),
]