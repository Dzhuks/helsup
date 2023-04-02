from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser


class OrderManager(models.Manager):
    def get_incompleted_orders(self):
        return super().get_queryset().filter(complited=False)


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="пользователь"
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
        return f"{self.price} тг"
