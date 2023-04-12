from django.core.validators import MinValueValidator
from django.db import models
from users.models import Client, Volunteer


class OrderManager(models.Manager):
    def get_incompleted_orders(self):
        return super().get_queryset().filter(completed=False)


# Create your models here.
class Order(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="my_orders",
        verbose_name="клиент",
    )
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="liked_orders",
        verbose_name="волонтер"
    )
    inquiry = models.CharField(
        max_length=100,
        verbose_name="запрос"
    )
    price = models.SmallIntegerField(
        validators=[MinValueValidator(100)],
        verbose_name="цена"
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="выполнено"
    )

    objects = OrderManager()

    @property
    def price_display(self):
        return f"{self.price}тг"
