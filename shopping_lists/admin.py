from django.contrib import admin
from django.utils.html import format_html
from .models import ShoppingList, ShoppingListItem


class ShoppingListItemInline(admin.TabularInline):
    model = ShoppingListItem
    fields = ("product_name", "price")
    extra = 0
    can_delete = True


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "status", "site_link")
    list_display_links = ("name",)
    list_editable = ("status",)
    search_fields = ("name",)
    list_filter = ("status", "created_at")
    ordering = ("-created_at", "id")
    list_per_page = 20
    inlines = (ShoppingListItemInline,)
    readonly_fields = ("id", "slug")
    view_on_site = True

    @admin.display(description="Страница на сайте")
    def site_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Открыть</a>',
            obj.get_absolute_url(),
        )


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price", "shopping_list")
    list_display_links = ("product_name",)
    search_fields = ("product_name", "shopping_list__name")
    list_filter = ("shopping_list",)
    ordering = ("id",)
    list_per_page = 20
    list_select_related = ("shopping_list",)
    autocomplete_fields = ("shopping_list",)
    