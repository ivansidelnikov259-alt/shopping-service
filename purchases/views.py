"""
View-функции приложения purchases.
"""
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from datetime import datetime
from .forms import PurchaseForm, CategoryForm, StoreForm

from .models import Purchase, Category


def purchases(request):
    """Страница со списком всех покупок (с поиском, сортировкой и пагинацией)."""
    # 1. Получаем параметры из GET-запроса
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "date")
    
    # 2. Получаем все покупки из базы (с оптимизацией)
    purchases_list = list(Purchase.objects.select_related("category", "store").all())
    
    # 3. ПОИСК НА СТОРОНЕ PYTHON (100% игнорирует регистр для кириллицы)
    if query:
        query_lower = query.lower()
        filtered_list = []
        for p in purchases_list:
            # Безопасно проверяем каждое поле, даже если магазина нет
            product_name = p.product_name.lower() if p.product_name else ""
            category_name = p.category.name.lower() if p.category and p.category.name else ""
            store_name = p.store.name.lower() if p.store and p.store.name else ""
            
            if (query_lower in product_name) or (query_lower in category_name) or (query_lower in store_name):
                filtered_list.append(p)
        purchases_list = filtered_list
        
    # 4. СОРТИРОВКА НА СТОРОНЕ PYTHON
    if sort == "date":
        purchases_list.sort(key=lambda x: x.purchase_date, reverse=True)
    elif sort == "price":
        purchases_list.sort(key=lambda x: x.price, reverse=True)
    elif sort == "name":
        purchases_list.sort(key=lambda x: x.product_name.lower())
        
    # 5. Агрегация общей суммы
    total_sum = sum(p.price for p in purchases_list)

    # 6. Пагинация
    paginator = Paginator(purchases_list, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "purchases": page_obj,
        "page_obj": page_obj,
        "total_sum": total_sum,
        "query": query,
        "sort": sort,
    }
    return render(request, "purchases/purchase_list.html", context)


def purchase_detail(request, purchase_id):
    """Страница отдельной покупки."""
    try:
        purchase_id_int = int(purchase_id)
    except ValueError:
        return render(
            request,
            "purchases/purchase_detail.html",
            {"purchase": None},
            status=404,
        )

    purchase = get_object_or_404(
        Purchase.objects.select_related("category", "store"),
        pk=purchase_id_int
    )
    context = {"purchase": purchase}
    return render(request, "purchases/purchase_detail.html", context)


def purchase_search(request):
    """Страница поиска покупок по названию."""
    query = request.GET.get("q", "").strip()
    results = []
    
    if query:
        query_lower = query.lower()
        all_purchases = Purchase.objects.select_related("category", "store").all()
        for p in all_purchases:
            if query_lower in (p.product_name or "").lower():
                results.append(p)

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "purchases/search.html", context)


def purchases_statistics(request):
    """Страница статистики покупок."""
    # Группировка по категориям через annotate
    stats = Category.objects.annotate(
        purchases_count=Count("purchases"),
        total_sum=Sum("purchases__price")
    ).filter(purchases_count__gt=0).order_by("-total_sum")

    # Использование values() для получения только нужных полей
    top_purchases = Purchase.objects.select_related("category").values(
        "product_name", "price", "category__name"
    ).order_by("-price")[:5]

    # Агрегация общих данных
    total_data = Purchase.objects.aggregate(
        total_count=Count("id"),
        total_sum=Sum("price")
    )

    context = {
        "stats": stats,
        "top_purchases": top_purchases,
        "total_count": total_data["total_count"],
        "total_sum": total_data["total_sum"] or 0.0,
    }
    return render(request, "purchases/statistics.html", context)

# --- СОЗДАНИЕ И РЕДАКТИРОВАНИЕ ПОКУПКИ ---
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchases:list')
    else:
        form = PurchaseForm()
    return render(request, 'purchases/purchase_form.html', {'form': form, 'title': 'Добавить покупку'})

def purchase_edit(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('purchases:list')
    else:
        form = PurchaseForm(instance=purchase)
    return render(request, 'purchases/purchase_form.html', {'form': form, 'title': 'Редактировать покупку'})

def purchase_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, pk=purchase_id)
    if request.method == 'POST':
        purchase.delete()
        return redirect('purchases:list')
    return render(request, 'purchases/confirm_delete.html', {'object': purchase, 'title': 'Удалить покупку'})

# --- УПРАВЛЕНИЕ КАТЕГОРИЯМИ ---
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchases:list')
    else:
        form = CategoryForm()
    return render(request, 'purchases/purchase_form.html', {'form': form, 'title': 'Добавить категорию'})

# --- УПРАВЛЕНИЕ МАГАЗИНАМИ ---
def store_create(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchases:list')
    else:
        form = StoreForm()
    return render(request, 'purchases/purchase_form.html', {'form': form, 'title': 'Добавить магазин'})
