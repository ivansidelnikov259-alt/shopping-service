"""
View-функции главного приложения Shopping Service.

Содержит:
- page() — единый HTML-каркас всех страниц;
- index() — главная страница.
"""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """
    Сформировать HTML-каркас страницы.

    Args:
        title: Заголовок вкладки браузера.
        content: HTML-содержимое страницы.

    Returns:
        Готовая HTML-страница как строка.
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
    <footer class="container text-center text-muted mt-5 mb-3">
        <small>Shopping Service — ПР5, Django</small>
    </footer>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Главная страница приложения."""
    content = """
    <div class="jumbotron bg-white p-5 rounded shadow-sm">
        <h1 class="display-4">Shopping Service</h1>
        <p class="lead">Сервис учёта покупок и формирования списка покупок.</p>
        <hr class="my-4">
        <p>Основные разделы:</p>
        <a href="/purchases/" class="btn btn-primary me-2">
            Список покупок
        </a>
        <a href="/shopping_lists/" class="btn btn-secondary">
            Списки покупок
        </a>
    </div>
    """
    return HttpResponse(page("Shopping Service", content))