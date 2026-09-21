# Shopping Service - Сервис учёта покупок и формирования списка покупок

## Назначение

Консольное приложение для учёта личных покупок, планирования бюджета и создания списков покупок. Сервис помогает пользователям отслеживать расходы, анализировать покупательское поведение и планировать покупки перед походом в магазин.

## Целевая аудитория

- Люди, контролирующие расходы и ведущие семейный бюджет
- Семьи, планирующие совместные покупки
- Пользователи, стремящиеся к осознанному потреблению

## Предметная область

Учёт совершенных покупок, создание списков товаров, анализ расходов по категориям и магазинам, хранение истории покупок. Основные объекты предметной области: помещение, пользователь, бронирование.

## Основные сущности

- **Пользователь** — владелец покупок и списков
- **Покупка** — запись о совершённой покупке
- **Магазин** — торговая точка
- **Категория** — группа товаров по назначению
- **Список покупок** — планируемый набор товаров
- **Товар** — конкретный товар с названием и ценой

## Основные классы

### BaseEntity (абстрактный базовый класс)

Базовый класс для всех сущностей предметной области. Демонстрирует принципы ООП:
- **Инкапсуляция** — защищённые атрибуты `_id`, `_name`, доступ через `@property`;
- **Наследование** — все сущности наследуются от `BaseEntity`;
- **Полиморфизм** — метод `__str__` переопределяется в подклассах.

**Атрибуты:**
- `_id` — защищённый идентификатор
- `_name` — защищённое название

**Методы:**
- `id` (`@property`) — чтение идентификатора
- `name` (`@property` / setter) — чтение/запись названия
- `to_dict()` — абстрактный метод сериализации
- `__str__()` — абстрактное строковое представление
- `__eq__()`, `__hash__()` — сравнение и хеширование по ID

### Category — категория

**Атрибуты:**
- `id`, `name`

**Методы:**
- `__str__()` — строковое представление
- `to_dict()` — сериализация
- `from_data()` (`@classmethod`) — создание из словаря
- `validate_name()` (`@staticmethod`) — проверка названия

### Store — магазин

**Атрибуты:**
- `id`, `name`, `address`

**Методы:**
- `__str__()`, `to_dict()`, `from_data()`
- `address` (`@property` / setter)

### Product — товар

**Атрибуты:**
- `id`, `name`, `price`, `category`

**Методы:**
- `__str__()`, `to_dict()`, `from_data()`
- `price` (`@property` / setter)
- `category` (`@property` / setter)
- `is_expensive()` — проверка дороговизны
- `validate_price()` (`@staticmethod`)

### User — пользователь

**Атрибуты:**
- `id`, `name`, `email`

**Методы:**
- `__str__()`, `to_dict()`, `from_data()`
- `email` (`@property` / setter)
- `_validate_email()` (`@staticmethod`)
- `is_valid_email()`

### Purchase — покупка

**Атрибуты:**
- `id`, `name`, `product` (объект `Product`), `price`, `category` (объект `Category`), `store` (объект `Store`), `purchase_date`

**Методы:**
- `__str__()`, `to_dict()`, `from_data()`
- `product`, `price`, `category`, `store`, `purchase_date` (`@property`)
- `display_date` (`@property`) — дата в формате ДД.ММ.ГГГГ

### ShoppingList — список покупок

**Атрибуты:**
- `id`, `name`, `items` (список объектов `Product`), `created_at`, `is_completed`

**Методы:**
- `__str__()`, `to_dict()`, `from_data()`
- `add_item()`, `remove_item()`, `complete()`
- `items`, `created_at`, `is_completed` (`@property`)
- `total` (`@property`) — вычисляемая сумма

## Взаимодействие объектов

- **`Purchase`** содержит ссылки на объекты **`Product`**, **`Category`**, **`Store`** — данные связанных объектов доступны напрямую: `purchase.product.name`, `purchase.store.name`, `purchase.category.name`.
- **`ShoppingList`** содержит список объектов **`Product`** — товары добавляются методом `add_item()`, удаляются методом `remove_item()`.
- Все сущности наследуются от **`BaseEntity`** — единый интерфейс `id`, `name`, `__str__`, `to_dict`.

## Структура проекта
shopping-service/
├── main.py # Точка входа и меню
├── storage.py # JSON ↔ объекты
├── utils.py # Вспомогательные функции ввода
├── models/ # Классы предметной области
│ ├── init.py
│ ├── base.py # BaseEntity
│ ├── category.py
│ ├── store.py
│ ├── product.py
│ ├── purchase.py
│ ├── shopping_list.py
│ └── user.py
├── data/ # JSON-файлы с данными
├── tests/ # Тесты
│ ├── conftest.py
│ ├── test_models.py
│ └── test_project.py
├── README.md
├── requirements.txt
├── pytest.ini
├── .flake8
└── .gitignore

## Технологии

- Python 3.13
- JSON для хранения данных
- pytest для тестирования (17 тестов)
- flake8 для проверки стиля

## Установка и запуск

```bash
git clone https://github.com/ivansidelnikov259-alt/shopping-service.git
cd shopping-service

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python main.py
pytest tests/ -v