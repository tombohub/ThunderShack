# Generated by Django 3.0.6 on 2020-07-29 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0008_auto_20200721_0509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
