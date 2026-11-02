from django.urls import path
from . import views

app_name = "shopping_lists"

urlpatterns = [
    path("", views.shopping_lists, name="list"),
    path("create/", views.list_create, name="create"),              # Новый список
    path("search/", views.list_search, name="search"),
    path("<str:list_id>/", views.list_detail, name="detail"),
    path("<int:list_id>/edit/", views.list_edit, name="edit"),         # Редактирование
    path("<int:list_id>/delete/", views.list_delete, name="delete"),   # Удаление
    path("<int:list_id>/add_item/", views.item_create, name="add_item"), # Добавить товар в список
    path("<int:list_id>/delete_item/<int:item_id>/", views.item_delete, name="delete_item"),
    path("<int:list_id>/toggle/", views.toggle_status, name="toggle_status"),
]
