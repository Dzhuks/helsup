from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.services import get_incompleted_orders


def choice(request):
    template_name = "orders/choice.html"
    context = {}
    return render(request, template_name, context)


@login_required
def liked_orders(request):
    template_name = "orders/liked.html"
    context = {}
    return render(request, template_name, context)


@login_required
def my_orders(request):
    template_name = "orders/my_orders.html"
    context = {}
    return render(request, template_name, context)


@login_required
def show_orders(request):
    template_name = "orders/show_orders.html"
    context = {
        "orders": get_incompleted_orders(),
    }
    return render(request, template_name, context)
