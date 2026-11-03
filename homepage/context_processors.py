from purchases.models import Purchase, Category

def global_context(request):
    """
    Контекстный процессор для передачи общих данных во все шаблоны.
    """
    # Получаем количество покупок и категорий
    purchases_count = Purchase.objects.count()
    categories_count = Category.objects.count()

    return {
        "site_name": "Shopping Service",
        "purchases_count": purchases_count,
        "categories_count": categories_count,
    }
