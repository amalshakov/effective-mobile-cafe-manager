from django.db.models import Sum
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request

from api.serializers import OrderSerializer
from orders.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заказами (Order).
    Предоставляет CRUD-операции, поиск и endpoint для расчета выручки.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "table_number",
        "status",
    ]

    @action(detail=False, methods=["get"])
    def revenue(self, request: Request) -> Response:
        """Дополнительный endpoint - расчет выручки."""
        total_revenue = (
            Order.objects.filter(status="paid").aggregate(Sum("total_price"))[
                "total_price__sum"
            ]
            or 0
        )
        return Response({"total_revenue": total_revenue})
