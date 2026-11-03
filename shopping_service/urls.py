"""
Корневая конфигурация маршрутов Django-проекта Shopping Service.
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("purchases/", include("purchases.urls")),
    path("shopping_lists/", include("shopping_lists.urls")),
]

# Подключаем маршруты Django Debug Toolbar только в режиме отладки
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = "homepage.views.page_not_found"
