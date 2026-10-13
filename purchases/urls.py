"""
Маршруты приложения purchases.
"""

from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.purchases, name="list"),
    path("search/", views.purchase_search, name="search"),
    path("statistics/", views.purchases_statistics, name="statistics"),
    path("<str:purchase_id>/", views.purchase_detail, name="detail"),
]
