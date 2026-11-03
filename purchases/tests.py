from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Purchase, Category, Store


class PurchaseModelTest(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.category = Category.objects.create(name="Продукты")
        self.store = Store.objects.create(name="Пятерочка", address="ул. Ленина, 1")
        self.purchase = Purchase.objects.create(
            product_name="Молоко",
            price=100.0,
            category=self.category,
            store=self.store,
            purchase_date=date.today()
        )

    def test_purchase_creation(self):
        """Тест: проверка создания покупки и её полей"""
        self.assertEqual(self.purchase.product_name, "Молоко")
        self.assertEqual(self.purchase.price, 100.0)
        self.assertEqual(self.purchase.category.name, "Продукты")
        self.assertEqual(self.purchase.store.name, "Пятерочка")

    def test_purchase_list_view(self):
        """Тест: проверка доступности страницы списка покупок"""
        response = self.client.get(reverse('purchases:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Молоко")

    def test_generated_field(self):
        """Тест: проверка вычисляемого поля is_expensive"""
        # Покупка за 100 рублей не должна быть дорогой
        self.assertFalse(self.purchase.is_expensive)
        
        # Меняем цену на 1500 и проверяем
        self.purchase.price = 1500
        self.purchase.save()
        self.purchase.refresh_from_db()  # Обновляем данные из базы
        self.assertTrue(self.purchase.is_expensive)
