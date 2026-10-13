"""
View-функции приложения shopping_lists.

Читают данные из SQLite через db.database.
"""

from django.shortcuts import render

from db.database import execute_one, execute_query
from sql_queries_lists import (
    LIST_BY_ID,
    LIST_ITEMS,
    LIST_SEARCH,
    LISTS_ALL,
)


def shopping_lists(request):
    """Страница со списком всех списков покупок."""
    lists = execute_query(LISTS_ALL)
    context = {"shopping_lists": lists}
    return render(request, "shopping_lists/shopping_list_list.html", context)


def list_detail(request, list_id):
    """Страница отдельного списка покупок."""
    try:
        list_id_int = int(list_id)
    except (ValueError, TypeError):
        return render(
            request,
            "shopping_lists/shopping_list_detail.html",
            {"shopping_list": None, "items": []},
            status=404,
        )

    shopping_list = execute_one(LIST_BY_ID, [list_id_int])
    items = []
    if shopping_list is not None:
        items = execute_query(LIST_ITEMS, [list_id_int])

    context = {
        "shopping_list": shopping_list,
        "items": items,
    }
    return render(
        request,
        "shopping_lists/shopping_list_detail.html",
        context,
        status=404 if shopping_list is None else 200,
    )


def list_search(request):
    """Страница поиска списков по названию."""
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        pattern = f"%{query}%"
        results = execute_query(LIST_SEARCH, [pattern])

    context = {"query": query, "results": results}
    return render(request, "shopping_lists/search.html", context)
