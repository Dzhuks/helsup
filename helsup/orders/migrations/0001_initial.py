# Generated by Django 4.1.7 on 2023-04-02 14:49

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquiry', models.CharField(max_length=100, verbose_name='запрос')),
                ('price', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(100)], verbose_name='цена')),
                ('completed', models.BooleanField(default=False, verbose_name='выполнено')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
        ),
    ]
