"""
View-функции приложения purchases.

Читают данные из SQLite через db.database.
"""

from django.shortcuts import render

from db.database import execute_one, execute_query
from sql_queries import (
    PURCHASE_BY_ID,
    PURCHASE_SEARCH,
    PURCHASES_BY_CATEGORY,
    PURCHASES_LIST,
    PURCHASES_STATISTICS,
    PURCHASES_TOTAL_SUM,
)


def purchases(request):
    """Страница со списком всех покупок."""
    purchases_list = execute_query(PURCHASES_LIST)
    total = execute_one(PURCHASES_TOTAL_SUM)
    total_sum = total["total_sum"] if total and total["total_sum"] else 0.0

    context = {
        "purchases": purchases_list,
        "total_sum": total_sum,
    }
    return render(request, "purchases/purchase_list.html", context)


def purchase_detail(request, purchase_id):
    """Страница отдельной покупки."""
    try:
        purchase_id_int = int(purchase_id)
    except (ValueError, TypeError):
        return render(
            request,
            "purchases/purchase_detail.html",
            {"purchase": None},
            status=404,
        )

    purchase = execute_one(PURCHASE_BY_ID, [purchase_id_int])

    context = {"purchase": purchase}
    return render(
        request,
        "purchases/purchase_detail.html",
        context,
        status=404 if purchase is None else 200,
    )


def purchase_search(request):
    """Страница поиска покупок по названию (параметризованный запрос)."""
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        pattern = f"%{query}%"
        results = execute_query(PURCHASE_SEARCH, [pattern])

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "purchases/search.html", context)


def purchases_statistics(request):
    """Страница статистики покупок (GROUP BY + COUNT + SUM)."""
    stats = execute_query(PURCHASES_STATISTICS)
    by_category = execute_query(PURCHASES_BY_CATEGORY)

    context = {
        "stats": stats,
        "by_category": by_category,
    }
    return render(request, "purchases/statistics.html", context)
