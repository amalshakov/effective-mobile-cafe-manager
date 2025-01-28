from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Order."""

    items = serializers.JSONField(help_text="Список блюд.")

    class Meta:
        model = Order
        fields = "__all__"

    def validate_items(
        self, value: list[dict[str, float]]
    ) -> list[dict[str, float]]:
        """Проверяем, что список блюд корректный."""
        if not isinstance(value, list) or not value:
            raise serializers.ValidationError(
                "Список блюд не может быть пустым."
            )

        for item in value:
            if (
                not isinstance(item, dict)
                or "name" not in item
                or "price" not in item
            ):
                raise serializers.ValidationError(
                    "Каждый элемент списка должен содержать 'name' и 'price'."
                )
            if not isinstance(item["name"], str) or not isinstance(
                item["price"], (int, float)
            ):
                raise serializers.ValidationError(
                    "Поле 'name' должно быть строкой, а 'price' числом."
                )
            if item["price"] <= 0:
                raise serializers.ValidationError(
                    "Цена блюда должна быть больше 0."
                )

        return value
