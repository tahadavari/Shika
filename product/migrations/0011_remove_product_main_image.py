# Generated by Django 3.2.6 on 2021-08-04 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_productimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='main_image',
        ),
    ]
