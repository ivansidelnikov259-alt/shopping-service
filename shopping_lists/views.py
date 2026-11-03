"""
View-функции приложения shopping_lists.
"""
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from .forms import ShoppingListForm, ShoppingListItemForm
from .models import ShoppingList, ShoppingListItem


def shopping_lists(request):
    """Страница со списком всех списков покупок."""
    lists = ShoppingList.objects.annotate(
        items_count=Count("items"),
        total_sum=Sum("items__price")
    ).order_by("-created_at")

    context = {"shopping_lists": lists}
    return render(request, "shopping_lists/shopping_list_list.html", context)


def list_detail(request, list_id):
    """Страница отдельного списка покупок."""
    shopping_list = get_object_or_404(
        ShoppingList.objects.prefetch_related("items"),
        pk=list_id
    )

    context = {
        "shopping_list": shopping_list,
        "items": shopping_list.items.all(),
    }
    return render(request, "shopping_lists/shopping_list_detail.html", context)


def list_search(request):
    """Страница поиска списков по названию."""
    query = request.GET.get("q", "").strip()
    results = ShoppingList.objects.none()

    if query:
        results = ShoppingList.objects.filter(name__icontains=query)

    context = {"query": query, "results": results}
    return render(request, "shopping_lists/search.html", context)


def list_create(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_list = form.save(commit=False)
            shopping_list.created_at = date.today()  # Устанавливаем текущую дату
            shopping_list.status = ShoppingList.Status.ACTIVE
            shopping_list.save()
            return redirect('shopping_lists:list')
    else:
        form = ShoppingListForm()
    return render(request, 'shopping_lists/list_form.html', {'form': form, 'title': 'Создать список'})


def list_edit(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    if request.method == 'POST':
        form = ShoppingListForm(request.POST, instance=shopping_list)
        if form.is_valid():
            form.save()
            return redirect('shopping_lists:list')
    else:
        form = ShoppingListForm(instance=shopping_list)
    return render(request, 'shopping_lists/list_form.html', {'form': form, 'title': 'Редактировать список'})   


def list_delete(request, list_id):
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    if request.method == 'POST':
        shopping_list.delete()
        return redirect('shopping_lists:list')
    return render(request, 'shopping_lists/confirm_delete.html', {'object': shopping_list, 'title': 'Удалить список'})


def item_create(request, list_id):
    """Добавление товара в список."""
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    if request.method == 'POST':
        form = ShoppingListItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.shopping_list = shopping_list
            item.save()
            return redirect('shopping_lists:detail', list_id=shopping_list.id)
    else:
        form = ShoppingListItemForm()
    return render(request, 'shopping_lists/item_form.html', {
        'form': form, 
        'title': 'Добавить товар в список', 
        'shopping_list': shopping_list
    })


def item_delete(request, list_id, item_id):
    """Удаление товара из списка."""
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    item = get_object_or_404(ShoppingListItem, pk=item_id, shopping_list=shopping_list)
    
    if request.method == 'POST':
        item.delete()
        return redirect('shopping_lists:detail', list_id=shopping_list.id)
    
    return render(request, 'shopping_lists/confirm_delete.html', {
        'object': item,
        'title': 'Удалить товар'
    })


def toggle_status(request, list_id):
    """Переключение статуса списка (активен/завершён)."""
    shopping_list = get_object_or_404(ShoppingList, pk=list_id)
    
    if shopping_list.status == ShoppingList.Status.ACTIVE:
        shopping_list.status = ShoppingList.Status.COMPLETED
    else:
        shopping_list.status = ShoppingList.Status.ACTIVE
        
    shopping_list.save()
    return redirect('shopping_lists:detail', list_id=shopping_list.id)
