from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum

from .models import Order
from .forms import OrderForm


def order_list(request):
    orders = Order.objects.all()
    query = request.GET.get("q")
    if query:
        orders = orders.filter(table_number=query) | orders.filter(
            status=query
        )
    return render(request, "orders/order_list.html", {"orders": orders})


def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderForm()
    return render(request, "orders/order_form.html", {"form": form})


def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("order_list")
    else:
        form = OrderForm(instance=order)
    return render(request, "orders/order_form.html", {"form": form})


def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect("order_list")
    return render(
        request, "orders/order_confirm_delete.html", {"order": order}
    )


def revenue_report(request):
    total_revenue = (
        Order.objects.filter(status="paid").aggregate(
            total=Sum("total_price")
        )["total"]
        or 0
    )
    return render(
        request, "orders/revenue_report.html", {"total_revenue": total_revenue}
    )
