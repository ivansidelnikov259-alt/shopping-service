"""
View-функции приложения shopping_lists.

Страницы:
- shopping_lists() — список списков покупок;
- list_detail() — один список покупок.
"""

from django.http import HttpResponse

from homepage.views import page
from storage import load_shopping_lists


def shopping_lists(request) -> HttpResponse:
    """Страница со списком всех списков покупок."""
    lists = load_shopping_lists()

    if not lists:
        content = """
        <h1>Списки покупок</h1>
        <div class="alert alert-info">
            Списков пока нет. Создайте их через консольное приложение.
        </div>
        """
        return HttpResponse(page("Списки покупок", content))

    items = ""
    for shopping_list in lists:
        items += f"""
        <li class="list-group-item d-flex justify-content-between align-items-center">
            <a href="/shopping_lists/{shopping_list.id}/">
                {shopping_list.name} ({len(shopping_list.items)} товаров)
            </a>
            <span class="badge bg-secondary">
                {shopping_list.total:.2f} руб.
            </span>
        </li>
        """

    content = f"""
    <h1>Списки покупок</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Списки покупок", content))


def list_detail(request, list_id: int) -> HttpResponse:
    """Страница отдельного списка покупок."""
    lists = load_shopping_lists()
    shopping_list = None
    for sl in lists:
        if sl.id == list_id:
            shopping_list = sl
            break

    if shopping_list is None:
        content = """
        <h1 class="text-danger">Список не найден</h1>
        <a href="/shopping_lists/" class="btn btn-outline-secondary">
            ← к спискам покупок
        </a>
        """
        return HttpResponse(
            page("Список не найден", content), status=404
        )

    items_html = ""
    for product in shopping_list.items:
        items_html += f"""
        <li class="list-group-item">
            {product.name} — {product.price:.2f} руб.
        </li>
        """

    if not items_html:
        items_html = '<li class="list-group-item">Список пуст</li>'

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h5 class="card-title">{shopping_list.name}</h5>
            <p class="card-text">
                <strong>Создан:</strong>
                {shopping_list.created_at.strftime('%d.%m.%Y')}
            </p>
            <ul class="list-group mb-3">{items_html}</ul>
            <p class="card-text">
                <strong>Итого:</strong>
                {shopping_list.total:.2f} руб.
            </p>
            <a href="/shopping_lists/" class="btn btn-outline-secondary">
                ← к спискам покупок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(shopping_list.name, content))