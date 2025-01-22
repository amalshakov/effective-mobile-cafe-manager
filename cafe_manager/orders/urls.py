from django.urls import path
from . import views

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.order_create, name="order_create"),
    path("<int:pk>/update/", views.order_update, name="order_update"),
    path("<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("revenue/", views.revenue_report, name="revenue_report"),
]
