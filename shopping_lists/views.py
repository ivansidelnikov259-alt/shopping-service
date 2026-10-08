"""
View-функции приложения shopping_lists.
"""

from django.shortcuts import render

from storage import load_shopping_lists


def shopping_lists(request):
    """Страница со списком всех списков покупок."""
    lists = load_shopping_lists()
    context = {
        "shopping_lists": lists,
    }
    return render(request, "shopping_lists/shopping_list_list.html", context)


def list_detail(request, list_id):
    """Страница отдельного списка покупок."""
    lists = load_shopping_lists()
    shopping_list = None
    for sl in lists:
        if sl.id == list_id:
            shopping_list = sl
            break

    context = {
        "shopping_list": shopping_list,
    }
    return render(
        request,
        "shopping_lists/shopping_list_detail.html",
        context,
        status=404 if shopping_list is None else 200,
    )
