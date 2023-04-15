from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=255,
        verbose_name='имя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='электронная почта',
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name='телефонный номер'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class Volunteer(CustomUser):
    class Meta:
        verbose_name = 'Волонтер'
        verbose_name_plural = 'Волонтеры'
        permissions = (("accept_order", "Can accept order"),)


class Client(CustomUser):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        permissions = (("create_order", "Can create order"),)


class BaseProfile(models.Model):
    AGE_MIN = 14
    AGE_MAX = 128

    class Sex(models.TextChoices):
        MALE = 'M', 'Мужской'
        FEMALE = 'F', 'Женский'
        OTHER = 'O', 'Другое'

    age = models.PositiveIntegerField(
        validators=[MinValueValidator(AGE_MIN), MaxValueValidator(AGE_MAX)],
        null=True, blank=True,
        verbose_name='возраст',
    )
    sex = models.CharField(
        max_length=1,
        choices=Sex.choices,
        null=True, blank=True,
        verbose_name='пол',
    )
    city = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name='город'
    )
    about_me = models.TextField(
        null=True, blank=True,
        verbose_name='о себе'
    )
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def city_display(self):
        return f"Адрес: {self.city}"


class VolunteerProfile(BaseProfile):
    volunteer = models.OneToOneField(Volunteer, on_delete=models.CASCADE, related_name='profile')


class ClientProfile(BaseProfile):
    class Mobility(models.TextChoices):
        NO = "Нету", "Люди, не имеющие ограничений по мобильности"
        M1 = "M1", "Люди, не имеющие инвалидности со сниженной мобильностью (люди пенсионного возраста, люди с детьми дошкольного возраста, беременные женщины), а также глухие и слабослышащие"
        M2 = "M2", "Пожилые немощные люди (в том числе инвалиды по старости), инвалиды с недостатками зрения, пользующиеся белой тростью"
        M3 = "M3", "Инвалиды и другие маломобильные граждане, не относящиеся к группе М2, использующие при движении дополнительные опоры (костыли, трости), инвалиды на протезах"
        M4 = "M4", "Инвалиды и другие маломобильные граждане, не относящиеся к группе М2, передвигающиеся на креслах-колясках"
        HM = "HM", "Немобильные граждане"
        HT = "HT", "Нетранспортабельные люди"
        HO = "HO", "Люди с ограниченной степенью свободы, в том числе люди с психическими отклонениями"

    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='profile')
    mobility = models.CharField(
        max_length=4,
        choices=Mobility.choices,
        null=True, blank=True,
        verbose_name='мобильность'
    )

    @property
    def mobility_display(self):
        if self.mobility == 'Нету':
            return 'Нету мобильности'
        return f'Группа мобильности: {self.mobility}'


@receiver(post_save, sender=Volunteer)
def create_volunteer_profile(sender, instance, created, **kwargs):
    if created:
        VolunteerProfile.objects.create(volunteer=instance)


@receiver(post_save, sender=Client)
def create_client_profile(sender, instance, created, **kwargs):
    if created:
        ClientProfile.objects.create(client=instance)


@receiver(post_save, sender=Volunteer)
def save_volunteer_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Client)
def save_client_profile(sender, instance, **kwargs):
    instance.profile.save()
