from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orders.forms import OrderForm
from orders.services import get_incompleted_orders


@login_required
def liked_orders(request):
    template_name = "orders/liked.html"
    context = {}
    return render(request, template_name, context)


@login_required
def my_orders(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.client = request.user
            order.save()
            return redirect('orders:my_orders')
    else:
        order_form = OrderForm()

    template_name = "orders/my_orders.html"
    context = {
        "order_form": order_form
    }
    return render(request, template_name, context)


@login_required
def show_orders(request):
    template_name = "orders/show_orders.html"
    context = {
        "orders": get_incompleted_orders(),
    }
    return render(request, template_name, context)
