from django.contrib.auth.decorators import user_passes_test
from users.models import Client, Volunteer


def volunteer_required(function=None):
    """
    Decorator for views that checks if the user belongs to the Volunteer model.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and Volunteer.objects.filter(pk=u.pk).exists(),
        login_url='/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def client_required(function=None):
    """
    Decorator for views that checks if the user belongs to the Client model.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and Client.objects.filter(pk=u.pk).exists(),
        login_url='/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
