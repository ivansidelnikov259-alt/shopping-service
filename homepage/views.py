"""
View-функции главного приложения Shopping Service.
"""

from django.shortcuts import render


def index(request):
    """Главная страница приложения."""
    return render(request, "homepage/index.html")
