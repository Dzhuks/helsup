from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

SEX_CHOICES = [
    (0, 'Мужской'),
    (1, 'Женский')
]

MOBILITY_CHOICES = [
    ("Нету", "Люди, не имеющие ограничений по мобильности"),
    ("M1", "Люди, не имеющие инвалидности со сниженной мобильностью (люди пенсионного возраста, люди с детьми дошкольного возраста, беременные женщины), а также глухие и слабослышащие"),
    ("M2", "Пожилые немощные люди (в том числе инвалиды по старости), инвалиды с недостатками зрения, пользующиеся белой тростью"),
    ("M3", "Инвалиды и другие маломобильные граждане, не относящиеся к группе М2, использующие при движении дополнительные опоры (костыли, трости), инвалиды на протезах"),
    ("M4", "Инвалиды и другие маломобильные граждане, не относящиеся к группе М2, передвигающиеся на креслах-колясках"),
    ("HM", "Немобильные граждане"),
    ("HT", "Нетранспортабельные люди"),
    ("HO", "Люди с ограниченной степенью свободы, в том числе люди с психическими отклонениями"),
]


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Электронная почта должна быть установалена")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    last_name = None
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя'
    )
    email = models.EmailField(
        max_length=60,
        unique=True,
        verbose_name='электронная почта',
    )
    phone_number = models.CharField(
        max_length=12,
        verbose_name='телефонный номер',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "phone_number"]

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default.jpg',
        upload_to='users_images',
        null=True, blank=True,
        verbose_name='картинка'
    )
    age = models.SmallIntegerField(
        validators=[MinValueValidator(14), MaxValueValidator(130)],
        null=True, blank=True,
        verbose_name='возраст'
    )
    sex = models.SmallIntegerField(
        choices=SEX_CHOICES,
        null=True, blank=True,
        verbose_name='пол'
    )
    city = models.CharField(
        max_length=40,
        null=True, blank=True,
        verbose_name='регион'
    )
    mobility = models.CharField(
        max_length=10,
        choices=MOBILITY_CHOICES,
        null=True, blank=True,
        verbose_name="мобильность",
    )
    about_me = models.TextField(
        max_length=600,
        default='',
        blank=True,
        verbose_name='о себе',
    )
    rating = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True, blank=True,
        verbose_name='оценка'
    )

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
