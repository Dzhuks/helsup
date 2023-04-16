from django.core.validators import MinValueValidator
from django.db import models
from users.models import Client, Volunteer


class OrderManager(models.Manager):
    def get_incompleted_orders(self):
        return super().get_queryset().filter(is_completed=False)

    def get_free_orders(self):
        return self.get_incompleted_orders().filter(volunteer=None)

    def get_volunteer_orders(self, volunteer: Volunteer):
        return super().get_queryset().filter(volunteer=Volunteer).order_by("is_completed")

    def get_client_orders(self, client: Client):
        return super().get_queryset().filter(client=client).order_by("is_completed")


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
    is_completed = models.BooleanField(
        default=False,
        verbose_name="выполнено"
    )

    objects = OrderManager()

    @property
    def inquiry_display(self):
        return f"Запрос: {self.inquiry}"

    @property
    def price_display(self):
        return f"Цена: {self.price} тг"
