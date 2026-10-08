from django.urls import path

from . import views

app_name = "shopping_lists"

urlpatterns = [
    path("", views.shopping_lists, name="list"),
    path("<int:list_id>/", views.list_detail, name="detail"),
]
