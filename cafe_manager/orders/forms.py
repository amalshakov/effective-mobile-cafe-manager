# orders/forms.py
from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["table_number", "items", "status"]
        widgets = {
            "items": forms.Textarea(attrs={"rows": 3}),
            "status": forms.Select(choices=Order.STATUS_CHOICES),
        }
        labels = {
            "table_number": "Номер стола",
            "items": "Заказанные блюда (JSON формат)",
            "status": "Статус заказа",
        }
