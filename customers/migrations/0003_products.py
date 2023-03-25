# Generated by Django 4.0.5 on 2023-03-25 12:49

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_completeprofile_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('name', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=250)),
                ('discounted_price', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, null=True, populate_from='name')),
                ('ratings', models.CharField(max_length=255)),
                ('feedback', models.CharField(max_length=255)),
                ('stock_status', models.CharField(max_length=255)),
            ],
        ),
    ]
