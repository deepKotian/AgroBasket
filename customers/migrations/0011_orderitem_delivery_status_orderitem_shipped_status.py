# Generated by Django 4.0.5 on 2023-03-26 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0010_orderitem_username_alter_orderitem_modeofdelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='delivery_status',
            field=models.CharField(default='False', max_length=255),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='shipped_status',
            field=models.CharField(default='False', max_length=255),
        ),
    ]
