# Generated by Django 3.0.6 on 2020-06-20 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_auto_20200620_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]