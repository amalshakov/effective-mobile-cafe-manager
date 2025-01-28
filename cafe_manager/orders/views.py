from typing import Optional

from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import OrderForm
from .models import Order


def order_list(request: HttpRequest) -> HttpResponse:
    """Отображает список всех заказов."""
    orders = Order.objects.all()
    query = request.GET.get("q")
    if query:
        if query.isdigit():
            orders = orders.filter(table_number=query)
        else:
            orders = orders.filter(status=query)

    return render(request, "orders/order_list.html", {"orders": orders})


def order_create(
    request: HttpRequest, pk: Optional[int] = None
) -> HttpResponse:
    """
    Создает новый заказ или отображает форму для редактирования существующего.
    """
    if pk:
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(request.POST or None, instance=order)
    else:
        form = OrderForm(request.POST or None)
        order = None
    if form.is_valid():
        order = form.save(commit=False)
        order.save()
        return redirect("order_list")

    return render(
        request, "orders/order_form.html", {"form": form, "order": order}
    )


def order_update(request: HttpRequest, pk: int) -> HttpResponse:
    """Обновляет существующий заказ."""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderForm(instance=order)

    return render(request, "orders/order_form.html", {"form": form})


def order_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Удаляет заказ."""
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")

    return render(
        request, "orders/order_confirm_delete.html", {"order": order}
    )


def revenue_report(request: HttpRequest) -> HttpResponse:
    """Отображает отчет о выручке."""
    total_revenue = (
        Order.objects.filter(status="paid").aggregate(
            total=Sum("total_price")
        )["total"]
        or 0
    )

    return render(
        request, "orders/revenue_report.html", {"total_revenue": total_revenue}
    )
