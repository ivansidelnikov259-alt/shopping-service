from django.contrib import admin
from .models import Category, Store, Purchase


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")
    list_display_links = ("name",)
    search_fields = ("name", "address")
    ordering = ("name",)
    list_per_page = 20


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price", "is_expensive", "category", "store", "purchase_date")
    list_display_links = ("product_name",)
    search_fields = ("product_name", "category__name", "store__name")
    list_filter = ("category", "store", "purchase_date")
    ordering = ("-purchase_date", "id")
    list_per_page = 20
    list_select_related = ("category", "store")
    date_hierarchy = "purchase_date"
    autocomplete_fields = ("category", "store")
    
    # Поля только для чтения (ID и дата создания из TimeStampedModel)
    readonly_fields = ("id", "created_at", "updated_at")
