"""
View-функции приложения purchases.
"""

from django.shortcuts import render

from storage import load_purchases


def purchases(request):
    """Страница со списком всех покупок."""
    purchases_list = load_purchases()
    context = {
        "purchases": purchases_list,
    }
    return render(request, "purchases/purchase_list.html", context)


def purchase_detail(request, purchase_id):
    """Страница отдельной покупки."""
    purchases_list = load_purchases()
    purchase = None
    for p in purchases_list:
        if p.id == purchase_id:
            purchase = p
            break

    context = {
        "purchase": purchase,
    }
    return render(
        request,
        "purchases/purchase_detail.html",
        context,
        status=404 if purchase is None else 200,
    )
