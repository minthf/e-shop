# Generated by Django 3.2.5 on 2021-07-14 07:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'ordered'), (2, 'paid'), (3, 'shipped'), (4, 'failed')], default=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
