"""
Корневая конфигурация маршрутов Django-проекта Shopping Service.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("purchases/", include("purchases.urls")),
    path("shopping_lists/", include("shopping_lists.urls")),
]