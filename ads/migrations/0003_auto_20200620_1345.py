# Generated by Django 3.0.6 on 2020-06-20 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_auto_20200620_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='ads/images'),
        ),
    ]