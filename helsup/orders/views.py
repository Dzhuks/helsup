from django.shortcuts import render


def choice(request):
    template_name = "orders/choice.html"
    context = {}
    return render(request, template_name, context)


def liked_orders(request):
    template_name = "orders/liked.html"
    context = {}
    return render(request, template_name, context)


def my_orders(request):
    template_name = "orders/my_orders.html"
    context = {}
    return render(request, template_name, context)


def show_orders(request):
    template_name = "orders/show_orders.html"
    context = {}
    return render(request, template_name, context)