# Generated by Django 4.1.7 on 2023-04-13 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_client_alter_order_volunteer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='completed',
            new_name='is_completed',
        ),
    ]
