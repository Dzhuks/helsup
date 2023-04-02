from orders.models import Order


def get_incompleted_orders():
    return Order.objects.get_incompleted_orders()
