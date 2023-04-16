from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from orders.forms import OrderForm
from orders.models import Order
from users.decorators import client_required, volunteer_required


@volunteer_required
@login_required
def liked_orders(request):
    volunteer = request.user
    template_name = "orders/liked_orders.html"
    context = {
        "volunteer_orders": Order.objects.get_volunteer_orders(volunteer=volunteer)
    }
    return render(request, template_name, context)


@client_required
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
    print(request.path)
    if request.method == 'POST':
        if "take_order" in request.POST:
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            order.volunteer = request.user
            order.save()
            return redirect('orders:show_orders')
        elif request.POST.get("change_order"):  # You can use else in here too if there is only 2 submit types.
            pass

    template_name = "orders/show_orders.html"
    context = {
        "orders": Order.objects.get_free_orders(),
    }
    return render(request, template_name, context)
