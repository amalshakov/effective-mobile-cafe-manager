from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Order(models.Model):
    """
    Модель для представления заказа в кафе.
    Содержит информацию о номере стола, заказанных блюдах,
    общей стоимости, статусе и времени создания.
    """

    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]

    table_number = models.PositiveSmallIntegerField(
        verbose_name="Номер стола",
        validators=[MinValueValidator(1)],
    )
    items = models.JSONField(
        verbose_name="Заказанные блюда (с ценами)",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        verbose_name="Общая стоимость",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус заказа",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания заказа",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def clean(self) -> None:
        """Проверяет, что номер стола больше 0."""
        if self.table_number == 0:
            raise ValidationError("Номер стола должен быть больше 0.")

    def calculate_total_price(self) -> None:
        """
        Вычисляет и устанавливает общую стоимость заказа на основе списка блюд.
        """
        self.total_price = sum(item["price"] for item in self.items)

    def save(self, *args, **kwargs) -> None:
        """Сохраняет заказ, предварительно рассчитывая общую стоимость."""
        self.calculate_total_price()
        super().save(*args, **kwargs)
