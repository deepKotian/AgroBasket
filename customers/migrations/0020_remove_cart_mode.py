# Generated by Django 4.0.5 on 2023-03-26 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0019_cart_mode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='mode',
        ),
    ]
