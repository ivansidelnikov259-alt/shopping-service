"""
Маршруты приложения shopping_lists.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.shopping_lists, name="shopping_lists"),
    path("<int:list_id>/", views.list_detail, name="list_detail"),
]