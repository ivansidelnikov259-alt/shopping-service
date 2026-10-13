"""
View-функции главного приложения Shopping Service.

Содержит:
- page() — вспомогательный HTML-каркас (сохранён как демонстрация ПР5);
- index() — главная страница;
- page_not_found() — кастомный обработчик 404.
"""

from django.http import HttpResponse
from django.shortcuts import render


def page(title: str, content: str) -> str:
    """
    Вспомогательный HTML-каркас (демонстрация подхода из ПР5).

    В ПР6 страницы переведены на Django-шаблоны, но функция сохранена
    как учебный пример того, как формировался HTML в ПР5.
    """
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Shopping Service</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/purchases/">Покупки</a>
                <a class="nav-link" href="/shopping_lists/">Списки покупок</a>
            </div>
        </div>
    </nav>
    <main class="container">
        {content}
    </main>
</body>
</html>"""


def index(request):
    """Главная страница приложения."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """
    Кастомный обработчик ошибки 404.

    Активируется при DEBUG = False для любого ненайденного URL.
    """
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )
