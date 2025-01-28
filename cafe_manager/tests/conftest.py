import pytest
from orders.models import Order


@pytest.fixture
def create_test_orders():
    """Фикстура для создания тестовых заказов."""
    order1 = Order.objects.create(
        table_number=1,
        items=[{"name": "Пицца", "price": 800}],
        status="pending",
    )
    order2 = Order.objects.create(
        table_number=2, items=[{"name": "Паста", "price": 350}], status="ready"
    )
    order3 = Order.objects.create(
        table_number=3, items=[{"name": "Салат", "price": 200}], status="paid"
    )
    return [order1, order2, order3]


@pytest.fixture
def create_test_order():
    """Фикстура для создания тестового заказа."""
    order = Order.objects.create(
        table_number=1,
        status="pending",
        items=[{"name": "Пицца", "price": 800}],
    )
    return order
