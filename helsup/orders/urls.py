from django.urls import path
from orders import views

app_name = "orders"

urlpatterns = [
    path("liked", views.liked_orders, name="liked_orders"),
    path("my_orders", views.my_orders, name="my_orders"),
    path("show_orders", views.show_orders, name="show_orders"),
]
