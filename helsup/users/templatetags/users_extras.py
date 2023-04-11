from django import template

register = template.Library()


@register.filter
def is_instance(user, model_name):
    model = getattr(user, '__class__')
    print(model.__name__.lower())
    return model.__name__.lower() == model_name.lower()
