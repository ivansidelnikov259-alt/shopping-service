# Shopping Service — сервис учёта покупок и формирования списка покупок

Консольное приложение на Python с веб-интерфейсом на Django.

## 1. Назначение проекта

Shopping Service — учебное приложение для учёта личных покупок, планирования бюджета и создания списков покупок. Проект позволяет хранить сведения о покупках, категориях, магазинах и списках покупок, выполнять основные операции с этими объектами и предоставлять доступ к информации через веб-интерфейс Django.

Проект развивается поэтапно: консольная версия приложения дополняется веб-интерфейсом и постепенно переводится на возможности Django.

## 2. Используемые технологии

- Python 3.13
- Django 5.2
- Django Template Language (DTL)
- HTML5
- CSS3
- JavaScript
- Bootstrap 5.3
- JSON для хранения данных
- Git
- pytest
- flake8

## 3. Предметная область

В системе используются шесть основных сущностей:

- **Пользователь (User)** — идентификатор, имя, email;
- **Покупка (Purchase)** — идентификатор, товар, цена, категория, магазин, дата;
- **Магазин (Store)** — идентификатор, название, адрес;
- **Категория (Category)** — идентификатор, название;
- **Список покупок (ShoppingList)** — идентификатор, название, товары, дата создания, признак завершённости;
- **Товар (Product)** — идентификатор, название, цена, категория.

Для предметной области реализованы собственные Python-классы (пакет `models/`, ПР3).

На текущем этапе данные хранятся в JSON-файлах. Django ORM и база данных приложения пока не используются.

## 4. Структура проекта
shopping-service/
├── shopping_service/ # пакет конфигурации Django-проекта
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
├── homepage/ # Django-приложение: главная страница
│ ├── templates/
│ │ └── homepage/
│ │ └── index.html
│ ├── static/
│ │ └── homepage/
│ │ ├── css/
│ │ │ └── style.css
│ │ ├── js/
│ │ │ └── main.js
│ │ └── img/
│ │ └── logo.png
│ ├── urls.py
│ └── views.py
├── purchases/ # Django-приложение: покупки
│ ├── templates/
│ │ └── purchases/
│ │ ├── purchase_list.html
│ │ ├── purchase_detail.html
│ │ └── includes/
│ │ └── purchase_card.html
│ ├── urls.py
│ └── views.py
├── shopping_lists/ # Django-приложение: списки покупок
│ ├── templates/
│ │ └── shopping_lists/
│ │ ├── shopping_list_list.html
│ │ ├── shopping_list_detail.html
│ │ └── includes/
│ │ └── status.html
│ ├── urls.py
│ └── views.py
├── templates/ # шаблоны уровня проекта
│ ├── base.html
│ └── includes/
│ └── navigation.html
├── models/ # классы предметной области (ПР3)
│ ├── init.py
│ ├── base.py
│ ├── category.py
│ ├── store.py
│ ├── product.py
│ ├── purchase.py
│ ├── shopping_list.py
│ └── user.py
├── data/ # JSON-файлы с данными
│ ├── purchases.json
│ ├── shopping_lists.json
│ ├── categories.json
│ └── stores.json
├── tests/ # тесты предметной области
│ ├── conftest.py
│ ├── test_models.py
│ └── test_project.py
├── main.py # консольная версия приложения
├── storage.py # загрузка/сохранение JSON
├── utils.py # вспомогательные функции
├── manage.py # управление Django-проектом
├── requirements.txt
├── pytest.ini
├── .flake8
├── .gitignore
└── README.md

text

## 5. Веб-интерфейс

Веб-часть приложения реализована на Django. Основные страницы:

| URL | View-функция | Назначение |
|-----|--------------|------------|
| `/` | `homepage.views.index` | Главная страница |
| `/purchases/` | `purchases.views.purchases` | Список всех покупок |
| `/purchases/<int:purchase_id>/` | `purchases.views.purchase_detail` | Страница отдельной покупки |
| `/shopping_lists/` | `shopping_lists.views.shopping_lists` | Список всех списков покупок |
| `/shopping_lists/<int:list_id>/` | `shopping_lists.views.list_detail` | Страница отдельного списка |

Если объект с указанным ID не найден — возвращается страница с HTTP-статусом **404**.

Для формирования страниц используются **Django-шаблоны**. Генерация HTML непосредственно в Python-коде веб-представлений не используется. Функция `page()` из ПР5 удалена.

Представления подготавливают данные и передают их в шаблоны через **контекст**.

## 6. Django Template Language

Шаблоны используют возможности Django Template Language.

### 6.1. Базовый шаблон

Общий шаблон страниц: `templates/base.html`.

Он содержит общую HTML-структуру страницы, подключение стилей и JavaScript, навигацию и блоки для содержимого отдельных страниц.

Дочерние шаблоны используют наследование:

```django
{% extends "base.html" %}
Содержимое отдельных страниц размещается в блоке:

django
{% block content %}
{% endblock %}
Заголовок страницы задаётся через блок:

django
{% block title %}
{% endblock %}
6.2. Включаемые шаблоны
Повторяющиеся фрагменты вынесены в отдельные шаблоны:

templates/includes/navigation.html — навигация;

purchases/templates/purchases/includes/purchase_card.html — карточка покупки;

shopping_lists/templates/shopping_lists/includes/status.html — статус списка.

Подключение выполняется с помощью:

django
{% include "purchases/includes/purchase_card.html" %}
или:

django
{% include "shopping_lists/includes/status.html" %}
6.3. Контекст
Представления передают данные в шаблоны через словарь контекста. Например, для списка покупок:

python
context = {
    "purchases": purchases_list,
}
В шаблоне данные доступны по имени переменной:

django
{% for purchase in purchases %}
6.4. Циклы и условия
Для формирования списков используются циклы:

django
{% for purchase in purchases %}
    ...
{% empty %}
    <p>Покупок пока нет.</p>
{% endfor %}
Условия используются для отображения различного содержимого страницы:

django
{% if purchase %}
    ...
{% else %}
    <h1>Покупка не найдена</h1>
{% endif %}
6.5. Фильтры шаблонов
В шаблонах используются стандартные фильтры Django Template Language:

{{ purchases|length }} — количество элементов;

{{ purchase.product.name|default:"Без названия" }} — значение по умолчанию;

{{ purchase.price|floatformat:2 }} — форматирование числа;

{{ purchase.purchase_date|date:"d.m.Y" }} — форматирование даты.

Фильтры используются для представления данных и не содержат бизнес-логику приложения.

6.6. URL-маршрутизация
Для страниц используются именованные маршруты Django:

django
{% url 'purchases:list' %}
{% url 'purchases:detail' purchase.id %}
{% url 'shopping_lists:list' %}
{% url 'shopping_lists:detail' shopping_list.id %}
Для приложений используются пространства имён (namespace):

homepage:index

purchases:list, purchases:detail

shopping_lists:list, shopping_lists:detail

Ссылки в шаблонах формируются через {% url %}, а не за счёт жёстко заданных адресов.

7. Статические файлы
Статические файлы проекта находятся в каталоге:

text
homepage/static/homepage/
Используются:

css/style.css — собственные стили;

js/main.js — автоматическая подстановка текущего года в подвал;

img/logo.png — логотип в навигации.

Для работы со статическими файлами в шаблонах используется:

django
{% load static %}
CSS подключается через:

django
{% static 'homepage/css/style.css' %}
Изображение:

django
{% static 'homepage/img/logo.png' %}
JavaScript:

django
{% static 'homepage/js/main.js' %}
В проекте используется собственный CSS для оформления элементов интерфейса (карточки покупок, статусы списков, подвал).

JavaScript используется для небольшого динамического поведения интерфейса — автоматического отображения текущего года в подвале страницы.

8. Хранение данных
На текущем этапе данные приложения хранятся в JSON-файлах:

data/purchases.json

data/shopping_lists.json

data/categories.json

data/stores.json

Загрузка данных выполняется средствами модуля storage.py.

Предметные объекты создаются на основе собственных Python-классов из каталога models/.

Django ORM на текущем этапе не используется.

9. Основные модули
storage.py
Отвечает за загрузку и сохранение данных. Выполняет преобразование:

JSON → объекты Python;

объекты Python → JSON.

models/
Содержит классы предметной области: BaseEntity, Category, Store, Product, Purchase, ShoppingList, User.

main.py
Содержит консольный вариант работы с приложением (сохранён с ПР1–ПР3).

utils.py
Содержит вспомогательные функции для консольного интерфейса.

purchases/views.py
Обрабатывает веб-запросы, связанные с покупками.

shopping_lists/views.py
Обрабатывает веб-запросы, связанные со списками покупок.

homepage/views.py
Содержит представление главной страницы.

10. Тестирование
В каталоге tests/ находятся тесты основных классов предметной области.

Для запуска тестов используется:

bash
pytest tests/ -v
Все 17 тестов проходят успешно.

11. Проверка качества кода
Для проверки соответствия кода требованиям форматирования и стиля используется flake8.

Запуск проверки:

bash
flake8 . --extend-exclude=venv
12. Запуск проекта
Веб-версия (Django)
bash
python manage.py runserver
После запуска веб-интерфейс доступен по адресу:

text
http://127.0.0.1:8000/
Консольная версия (сохранена)
bash
python main.py
13. Работа с Git
Исходный код проекта хранится в Git-репозитории.

Пример фиксации изменений:

bash
git status
git add .
git commit -m "PR6: switch web interface to Django templates and static files"
git push origin main
14. Текущее состояние проекта
На текущем этапе Shopping Service содержит:

предметные классы BaseEntity, Category, Store, Product, Purchase, ShoppingList, User;

консольный интерфейс (main.py);

хранение данных в JSON;

Django-проект shopping_service с приложениями homepage, purchases, shopping_lists;

веб-представления для основных сущностей;

Django Template Language;

наследование шаблонов (base.html);

блоки шаблонов (block);

включаемые шаблоны (include);

циклы (for) и условия (if);

фильтры шаблонов;

именованные URL и namespaces;

статические CSS, JavaScript и графический файл;

собственное оформление интерфейса;

тесты предметной области (17 тестов).

Формы Django, модели Django ORM и работа с базой данных в текущей версии проекта не реализованы.

15. Дальнейшее развитие
Следующие этапы развития проекта предполагают:

переход от хранения данных в JSON к использованию базы данных и Django ORM;

реализацию форм Django;

добавление операций создания, изменения и удаления объектов через веб-интерфейс;

обработку пользовательского ввода и валидацию данных;

регистрацию и аутентификацию пользователей;

разработку REST API;

контейнеризацию приложения в Docker;

настройку CI/CD.