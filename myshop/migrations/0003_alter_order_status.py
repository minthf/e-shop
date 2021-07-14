# Generated by Django 3.2.5 on 2021-07-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myshop', '0002_auto_20210714_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered'), ('paid', 'paid'), ('shipped', 'shipped'), ('failed', 'failed')], default='ordered', max_length=8),
        ),
    ]