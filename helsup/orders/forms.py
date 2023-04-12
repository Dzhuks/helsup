from django.forms import ModelForm
from orders.models import Order


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "theform__input"
            field.field.widget.attrs["type"] = "text"
            field.field.widget.attrs["placeholder"] = field.label

    class Meta:
        model = Order
        fields = ["inquiry", "price"]
