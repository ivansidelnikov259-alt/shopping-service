from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("", views.purchases, name="list"),
    path("<int:purchase_id>/", views.purchase_detail, name="detail"),
]
