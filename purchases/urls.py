from django.urls import path
from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.purchases, name="list"),
    path("create/", views.purchase_create, name="create"),         # Новая покупка
    path("category/create/", views.category_create, name="category_create"), # Новая категория
    path("store/create/", views.store_create, name="store_create"),        # Новый магазин
    path("search/", views.purchase_search, name="search"),
    path("statistics/", views.purchases_statistics, name="statistics"),
    path("<str:purchase_id>/", views.purchase_detail, name="detail"),
    path("<int:purchase_id>/edit/", views.purchase_edit, name="edit"),     # Редактирование
    path("<int:purchase_id>/delete/", views.purchase_delete, name="delete"), # Удаление
]
