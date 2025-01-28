import pytest
from django.urls import reverse
from orders.models import Order


@pytest.mark.django_db
def test_list_view(client, create_test_orders):
    """Тест для order_list без параметров запроса и с параметрами."""
    response = client.get(reverse("order_list"))
    assert response.status_code == 200

    # Проверяем, что правильный шаблон рендерится
    assert "orders/order_list.html" in [t.name for t in response.templates]

    # Проверяем, что используется правильная вьюха
    assert response.resolver_match.func.__name__ == "order_list"

    # Проверяем контекст
    assert len(response.context["orders"]) == 3

    # Проверяем HTML-вывод
    content = response.content.decode("utf-8")
    assert "Список заказов" in content
    assert "Пицца" in content
    assert "Паста" in content
    assert "Салат" in content

    # Проверяем фильтрацию по номеру стола
    response = client.get(reverse("order_list"), {"q": "1"})
    assert response.status_code == 200
    assert len(response.context["orders"]) == 1
    assert response.context["orders"][0].table_number == 1
    assert "Пицца" in response.content.decode("utf-8")
    assert "Паста" not in response.content.decode("utf-8")

    # Проверяем фильтрацию по статусу
    response = client.get(reverse("order_list"), {"q": "ready"})
    assert response.status_code == 200
    assert len(response.context["orders"]) == 1
    assert response.context["orders"][0].status == "ready"
    assert "Паста" in response.content.decode("utf-8")
    assert "Пицца" not in response.content.decode("utf-8")

    # Проверяем фильтрацию по несуществующему запросу
    response = client.get(reverse("order_list"), {"q": "nonexistent"})
    assert response.status_code == 200
    assert len(response.context["orders"]) == 0
    assert "Заказы отсутствуют" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_order_create_view_get(client):
    """Тест отображения формы создания нового заказа (GET-запрос)."""
    response = client.get(reverse("order_create"))
    assert response.status_code == 200

    # Проверяем, что правильный шаблон рендерится
    assert "orders/order_form.html" in [t.name for t in response.templates]

    # Проверяем, что форма присутствует в ответе
    content = response.content.decode("utf-8")
    assert "Создание нового заказа" in content
    assert '<form method="post">' in content


@pytest.mark.django_db
def test_order_create_view_post_valid_data(client):
    """Тест создания нового заказа с валидными данными (POST-запрос)."""
    data = {
        "table_number": 4,
        "status": "pending",
        "items_text": "борщ 100\nсок 50",
    }

    response = client.post(reverse("order_create"), data=data)

    # После успешного создания должен быть редирект
    assert response.status_code == 302
    assert response.url == reverse("order_list")

    # Проверяем, что заказ создан
    order = Order.objects.get(table_number=4)
    assert order.table_number == 4
    assert order.status == "pending"
    assert order.total_price == 150
    assert len(order.items) == 2
    assert order.items[0]["name"] == "борщ"
    assert order.items[1]["price"] == 50


@pytest.mark.django_db
def test_order_create_view_post_invalid_data(client):
    """Тест создания нового заказа с невалидными данными (POST-запрос)."""
    data = {
        "table_number": 1,
        "status": "pending",
        "items_text": "невалидная строка",  # Некорректная строка
    }

    response = client.post(reverse("order_create"), data=data)

    # Проверяем, что статус код 200 (форма рендерится с ошибками)
    assert response.status_code == 200

    # Проверяем, что ошибки отобразились
    content = response.content.decode("utf-8")
    assert "Некорректный формат строки" in content

    # Убедимся, что заказ не создан
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_order_update_view_get(client, create_test_order):
    """Тест отображения формы обновления заказа (GET-запрос)."""
    response = client.get(
        reverse("order_update", kwargs={"pk": create_test_order.pk})
    )
    assert response.status_code == 200

    # Проверяем, что правильный шаблон рендерится
    assert "orders/order_form.html" in [t.name for t in response.templates]

    # Проверяем, что форма заполнена данными заказа
    content = response.content.decode("utf-8")
    assert f'value="{create_test_order.table_number}"' in content
    assert f'value="{create_test_order.status}"' in content


@pytest.mark.django_db
def test_order_update_view_post_valid_data(client, create_test_order):
    """Тест обновления заказа с валидными данными (POST-запрос)."""
    data = {
        "table_number": 2,
        "status": "ready",
        "items_text": "Пицца 200\nсок 100",
    }

    response = client.post(
        reverse("order_update", kwargs={"pk": create_test_order.pk}), data=data
    )

    # Проверяем, что произошел редирект
    assert response.status_code == 302
    assert response.url == reverse("order_list")

    # Проверяем, что данные заказа обновлены
    create_test_order.refresh_from_db()
    assert create_test_order.table_number == 2
    assert create_test_order.status == "ready"
    assert create_test_order.total_price == 300
    assert len(create_test_order.items) == 2
    assert create_test_order.items[0]["name"] == "Пицца"
    assert create_test_order.items[1]["price"] == 100


@pytest.mark.django_db
def test_order_update_view_post_invalid_data(client, create_test_order):
    """Тест обновления заказа с невалидными данными (POST-запрос)."""
    # Данные с ошибками
    data = {
        "table_number": "",  # Некорректный номер стола
        "status": "pending",
        "items_text": "невалидная строка",  # Некорректный формат блюд
    }

    response = client.post(
        reverse("order_update", kwargs={"pk": create_test_order.pk}), data=data
    )

    # Проверяем, что статус код 200 (форма рендерится с ошибками)
    assert response.status_code == 200

    # Проверяем, что ошибки отображаются
    content = response.content.decode("utf-8")
    assert (
        "Обязательное поле" in content
        or "Некорректный формат строки" in content
    )

    # Убедимся, что данные заказа не изменились
    create_test_order.refresh_from_db()
    assert create_test_order.table_number == 1
    assert create_test_order.status == "pending"
    assert create_test_order.items == [{"name": "Пицца", "price": 800}]


@pytest.mark.django_db
def test_order_delete_view_get(client, create_test_order):
    """Тест отображения страницы подтверждения удаления заказа (GET-запрос)."""
    response = client.get(
        reverse("order_delete", kwargs={"pk": create_test_order.pk})
    )

    # Проверяем, что страница подтверждения загрузилась
    assert response.status_code == 200
    assert "orders/order_confirm_delete.html" in [
        t.name for t in response.templates
    ]

    # Проверяем, что текст подтверждения отображается
    content = response.content.decode("utf-8")
    assert "Вы уверены, что хотите удалить заказ" in content
    assert "Пицца" in content


@pytest.mark.django_db
def test_order_delete_view_post(client, create_test_order):
    """Тест успешного удаления заказа (POST-запрос)."""
    response = client.post(
        reverse("order_delete", kwargs={"pk": create_test_order.pk})
    )

    # Проверяем, что произошел редирект на список заказов
    assert response.status_code == 302
    assert response.url == reverse("order_list")

    # Убедимся, что заказ удален
    with pytest.raises(Order.DoesNotExist):
        Order.objects.get(pk=create_test_order.pk)


@pytest.mark.django_db
def test_order_delete_view_invalid_id(client):
    """Тест попытки удаления заказа с несуществующим ID."""
    response = client.get(reverse("order_delete", kwargs={"pk": 999}))
    assert response.status_code == 404


@pytest.mark.django_db
def test_revenue_report_no_orders(client):
    """Тест отображения отчета о выручке, если нет заказов."""
    response = client.get(reverse("revenue_report"))

    assert response.status_code == 200
    assert "orders/revenue_report.html" in [t.name for t in response.templates]

    # Проверяем, что выручка равна 0
    content = response.content.decode("utf-8")
    assert (
        "Общая выручка за оплаченные заказы: <strong>0,00 ₽</strong" in content
    )


@pytest.mark.django_db
def test_revenue_report_with_paid_orders(client):
    """Тест отображения отчета о выручке, если есть оплаченные заказы."""
    Order.objects.create(
        table_number=1,
        items=[{"name": "пицца", "price": 500}],
        status="paid",
    )
    Order.objects.create(
        table_number=2,
        items=[{"name": "салат", "price": 300}],
        status="paid",
    )
    Order.objects.create(
        table_number=3,
        items=[{"name": "бургер", "price": 200}],
        status="pending",  # Не оплаченный заказ
    )

    response = client.get(reverse("revenue_report"))

    assert response.status_code == 200

    # Проверяем, что выручка корректно отображается
    content = response.content.decode("utf-8")
    assert (
        "Общая выручка за оплаченные заказы: <strong>800,00 ₽</strong"
        in content
    )


@pytest.mark.django_db
def test_revenue_report_only_pending_orders(client):
    """Тест отображения отчета о выручке, если оплаченных заказов нет."""
    Order.objects.create(
        table_number=1,
        items=[{"name": "кофе", "price": 100}],
        status="pending",
    )
    Order.objects.create(
        table_number=2,
        items=[{"name": "чай", "price": 50}],
        status="pending",
    )

    response = client.get(reverse("revenue_report"))

    assert response.status_code == 200

    # Проверяем, что выручка равна 0
    content = response.content.decode("utf-8")
    assert (
        "Общая выручка за оплаченные заказы: <strong>0,00 ₽</strong" in content
    )
