from django import template

register = template.Library()


@register.filter
def is_instance(user, model_name):
    model = getattr(user, '__class__')
    return model.__name__.lower() == model_name.lower()
