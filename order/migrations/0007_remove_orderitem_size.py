# Generated by Django 3.2.6 on 2021-08-10 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_orderitem_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
    ]
