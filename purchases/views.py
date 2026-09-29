"""
View-функции приложения purchases.

Страницы:
- purchases() — список покупок;
- purchase_detail() — одна покупка.
"""

from django.http import HttpResponse

from homepage.views import page
from storage import load_purchases


def purchases(request) -> HttpResponse:
    """Страница со списком всех покупок."""
    purchases_list = load_purchases()
    if not purchases_list:
        content = """
        <h1>Покупки</h1>
        <div class="alert alert-info">
            Покупок пока нет. Добавьте их через консольное приложение.
        </div>
        """
        return HttpResponse(page("Покупки", content))

    items = ""
    total = 0.0
    for purchase in purchases_list:
        total += purchase.price
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/purchases/{purchase.id}/">
                {purchase.product.name} — {purchase.price:.2f} руб.
            </a>
            <span class="badge bg-secondary">
                {purchase.category.name}
            </span>
        </li>
        """

    content = f"""
    <h1>Покупки</h1>
    <p class="text-muted">
        Всего покупок: {len(purchases_list)}, общая сумма: {total:.2f} руб.
    </p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Покупки", content))


def purchase_detail(request, purchase_id: int) -> HttpResponse:
    """Страница отдельной покупки."""
    purchases_list = load_purchases()
    purchase = None
    for p in purchases_list:
        if p.id == purchase_id:
            purchase = p
            break

    if purchase is None:
        content = """
        <h1 class="text-danger">Покупка не найдена</h1>
        <a href="/purchases/" class="btn btn-outline-secondary">
            ← к списку покупок
        </a>
        """
        return HttpResponse(
            page("Покупка не найдена", content), status=404
        )

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h5 class="card-title">
                Покупка №{purchase.id}: {purchase.product.name}
            </h5>
            <p class="card-text">
                <strong>Цена:</strong> {purchase.price:.2f} руб.
            </p>
            <p class="card-text">
                <strong>Категория:</strong> {purchase.category.name}
            </p>
            <p class="card-text">
                <strong>Магазин:</strong> {purchase.store.name}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {purchase.display_date}
            </p>
            <a href="/purchases/" class="btn btn-outline-secondary">
                ← к списку покупок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Покупка №{purchase.id}", content))