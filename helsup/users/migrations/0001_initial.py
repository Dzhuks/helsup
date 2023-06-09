# Generated by Django 4.1.7 on 2023-04-09 14:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255, verbose_name='имя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='электронная почта')),
                ('phone_number', models.CharField(max_length=20, verbose_name='телефонный номер')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'permissions': (('create_order', 'Can create order'),),
            },
            bases=('users.customuser',),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Волонтер',
                'verbose_name_plural': 'Волонтеры',
                'permissions': (('accept_order', 'Can accept order'),),
            },
            bases=('users.customuser',),
        ),
        migrations.CreateModel(
            name='VolunteerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(14), django.core.validators.MaxValueValidator(128)], verbose_name='возраст')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский'), ('O', 'Другое')], max_length=1, null=True, verbose_name='пол')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='город')),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='о себе')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('volunteer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='users.volunteer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(14), django.core.validators.MaxValueValidator(128)], verbose_name='возраст')),
                ('sex', models.CharField(blank=True, choices=[('M', 'Мужской'), ('F', 'Женский'), ('O', 'Другое')], max_length=1, null=True, verbose_name='пол')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='город')),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='о себе')),
                ('rating', models.FloatField(blank=True, null=True)),
                ('mobility', models.CharField(blank=True, choices=[('Нету', 'Люди, не имеющие ограничений по мобильности'), ('M1', 'Люди, не имеющие инвалидности со сниженной мобильностью (люди пенсионного возраста, люди с детьми дошкольного возраста, беременные женщины), а также глухие и слабослышащие'), ('M2', 'Пожилые немощные люди (в том числе инвалиды по старости), инвалиды с недостатками зрения, пользующиеся белой тростью'), ('M3', 'Инвалиды и другие маломобильные граждане, не относящиеся к группе М2, использующие при движении дополнительные опоры (костыли, трости), инвалиды на протезах'), ('M4', 'Инвалиды и другие маломобильные граждане, не относящиеся к группе М2, передвигающиеся на креслах-колясках'), ('HM', 'Немобильные граждане'), ('HT', 'Нетранспортабельные люди'), ('HO', 'Люди с ограниченной степенью свободы, в том числе люди с психическими отклонениями')], max_length=4, null=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='users.client')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
