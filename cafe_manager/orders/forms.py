import re

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказов.
    Позволяет вводить список блюд с ценами в текстовом формате.
    """

    items_text = forms.CharField(
        label="Список блюд (построчно)",
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "борщ 100\nгречка 20\nсметана 15.0\nрис 25.70",
            }
        ),
        required=True,
        help_text="Введите список блюд с ценами",
    )

    class Meta:
        model = Order
        fields = ["table_number", "status"]

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализирует форму, устанавливая начальное значение
        для items_text при редактировании заказа.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            items = self.instance.items
            if items:
                # Преобразуем JSON в построчный текст
                self.fields["items_text"].initial = "\n".join(
                    f"{item['name']} {item['price']}" for item in items
                )
        self.fields["table_number"].widget.attrs.update({"min": 1})

    def clean_items_text(self) -> list[dict[str, float]]:
        """
        Проверяет и преобразует введенный текст
        в список словарей с блюдами и ценами.
        """
        data = self.cleaned_data["items_text"]
        items = []
        for line in data.splitlines():
            match = re.match(r"^(.+)\s+([\d]+(\.\d{1,2})?)$", line.strip())
            if not match:
                raise forms.ValidationError(
                    f"Некорректный формат строки: '{line}'. "
                    "Ожидается примерно следующее 'сметана 50'."
                )
            name, price = match.group(1), float(match.group(2))
            if price <= 0:
                raise forms.ValidationError("Цена блюда должна быть больше 0.")
            items.append({"name": name, "price": price})
        return items

    def save(self, commit: bool = True) -> Order:
        """
        Сохраняет форму, преобразуя текст блюд в JSON
        и вычисляя общую цену заказа.
        """
        items = self.cleaned_data.get("items_text", [])
        self.instance.items = items
        self.instance.calculate_total_price()
        return super().save(commit=commit)
