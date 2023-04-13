from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orders.forms import OrderForm
from orders.models import Order


@login_required
def liked_orders(request):
    template_name = "orders/liked.html"
    context = {
        "volunteer_orders": Order.objects.get_volunteer_orders()
    }
    return render(request, template_name, context)


@login_required
def my_orders(request):
    client = request.user
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.client = client
            order.save()
            return redirect('orders:my_orders')
    else:
        order_form = OrderForm()

    template_name = "orders/my_orders.html"
    context = {
        "order_form": order_form,
        "client_orders": Order.objects.get_client_orders(client=client),
    }
    return render(request, template_name, context)


@login_required
def show_orders(request):
    template_name = "orders/show_orders.html"
    context = {
        "orders": Order.objects.get_incompleted_orders(),
    }
    return render(request, template_name, context)
