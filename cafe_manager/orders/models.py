from django.db import models
from django.core.exceptions import ValidationError


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]

    table_number = models.IntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Заказанные блюда (с ценами)")
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
        verbose_name="Время создания",
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id} - Стол {self.table_number}"

    def clean(self):
        super().clean()
        if self.total_price <= 0:
            raise ValidationError(
                f"Общая стоимость заказа должна быть больше 0"
            )

    def save(self, *args, **kwargs):
        total_price = sum(item["price"] for item in self.items)
        self.total_price = total_price
        super().save(*args, **kwargs)
