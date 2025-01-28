# effective-mobile-cafe-manager

**Ссылка на тестовое задание:**  
[Тестовое задание](https://docs.google.com/document/d/1-VJZRZhaWjtcqN-edMS2EKp621eMHqho9hPaZWSe8Og/edit?tab=t.0#heading=h.c8vqchg2yga1)

## Описание приложения

Полнофункциональное веб-приложение на Django для управления заказами в кафе.  
Приложение позволяет добавлять, удалять, искать, изменять и отображать заказы.

## Стек технологий

- **Python**
- **Django**
- **Django REST framework**
- **Pytest**

## Установка и запуск

1. **Клонируйте репозиторий**:
```
git clone git@github.com:amalshakov/effective-mobile-cafe-manager.git
```
2. **Создайте и активируйте виртуальное окружение**:
```
python -m venv venv
source venv/Scripts/activate
```
3. **Установите зависимости**:
```
pip install -r .\requirements.txt
```
4. **Запустите docker-compose (postgres db)**:
```
docker-compose up
```
5. **Перейдите в папку проекта, создайте и примените миграции**:
```
cd cafe_manager
python manage.py makemigrations
python manage.py migrate
```
6. **Если планируете работать через админку, создайте суперпользователя**:
```
python manage.py createsuperuser
```
7. **Запустите сервер локально**:
```
python manage.py runserver
```

## Веб-интерфейс

*   **URL:** `http://127.0.0.1:8000/`
*   **Функциональность:**
    *   **Все заказы:**
        *   Отображает список всех заказов.
        *   Позволяет фильтровать заказы по номеру стола или статусу (pending, ready, paid).
        *   Позволяет редактировать заказ (включая изменение его статуса).
        *   Позволяет удалять заказ.
    *   **Создать заказ:** Позволяет создать новый заказ.
    *   **Выручка:** Отображает общую выручку за оплаченные заказы.

## Административный интерфейс

*   **URL:** `http://127.0.0.1:8000/admin`
*   **Функциональность:**
    *   Стандартный интерфейс администратора Django для управления моделями данных (пользователи, заказы и т.д.).

## REST API

*   **URL:** `http://127.0.0.1:8000/api/`
*   **Эндпоинты:**

    *   **Получение списка заказов:**
        *   **Метод:** `GET`
        *   **URL:** `http://127.0.0.1:8000/api/orders/`
        *   **Пример ответа:**

            ```json
            [
                {
                    "id": 3,
                    "items": [
                        {
                            "name": "рис",
                            "price": 70.0
                        },
                        {
                            "name": "гречка",
                            "price": 50.0
                        }
                    ],
                    "table_number": 2,
                    "total_price": "120.00",
                    "status": "paid",
                    "created_at": "2025-01-28T10:12:24.735882Z"
                },
                {
                    "id": 2,
                    "items": [
                        {
                            "name": "авокадо",
                            "price": 70.0
                        },
                        {
                            "name": "масло",
                            "price": 88.0
                        }
                    ],
                    "table_number": 1,
                    "total_price": "158.00",
                    "status": "ready",
                    "created_at": "2025-01-28T10:12:13.089675Z"
                },
                {
                    "id": 1,
                    "items": [
                        {
                            "name": "сок",
                            "price": 60.0
                        },
                        {
                            "name": "яблоко",
                            "price": 77.0
                        }
                    ],
                    "table_number": 1,
                    "total_price": "137.00",
                    "status": "paid",
                    "created_at": "2025-01-28T09:44:37.763576Z"
                }
            ]
            ```

        *   **Фильтрация по статусу:**
            *   **Метод:** `GET`
            *   **URL:** `http://127.0.0.1:8000/api/orders/?search=ready` (`ready`, `pending`, `paid`).
        *   **Фильтрация по номеру стола:**
            *   **Метод:** `GET`
            *   **URL:** `http://127.0.0.1:8000/api/orders/?search=2` (замените `2` на нужный номер стола).
    *   **Создание заказа:**
        *   **Метод:** `POST`
        *   **URL:** `http://127.0.0.1:8000/api/orders/`
        *   **Пример запроса (JSON body):**

            ```json
            {
                "table_number": 1,
                "items": [
                    {"name": "борщ", "price": 100},
                    {"name": "гречка", "price": 20.5}
                ],
                "status": "pending"
            }
            ```
    *   **Обновление заказа:**
        *   **Метод:** `PUT`
        *   **URL:** `http://127.0.0.1:8000/api/orders/<order_id>/` (замените `<order_id>` на ID заказа, который нужно обновить).
    *   **Удаление заказа:**
        *   **Метод:** `DELETE`
        *   **URL:** `http://127.0.0.1:8000/api/orders/<order_id>/` (замените `<order_id>` на ID заказа, который нужно удалить).
    *   **Получение дохода:**
        *   **Метод:** `GET`
        *   **URL:** `http://127.0.0.1:8000/api/orders/revenue/`
        *   **Пример ответа:**
            ```json
            {
                "total_revenue": 257.0
            }
            ```


### Автор:
- Александр Мальшаков (ТГ [@amalshakov](https://t.me/amalshakov), GitHub [amalshakov](https://github.com/amalshakov/))

### PS:
- .env добавлен в репу, для удобства (реальных секретных данных там нет)