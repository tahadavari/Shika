# Generated by Django 3.2.6 on 2021-08-08 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('creat_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Brand Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('creat_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Category Name')),
                ('icon', models.ImageField(default='category/icon/default.png', upload_to='category/icon', verbose_name='Icon')),
                ('image', models.ImageField(default='category/image/default.jpg', upload_to='category/image', verbose_name='Image')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='product.category', verbose_name='Parent')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('creat_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('percent', models.IntegerField(default=0, verbose_name='Percent')),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
                ('type', models.CharField(blank=True, choices=[('PR', 'Percent'), ('AM', 'Amount')], default=None, max_length=10, null=True, verbose_name='Type')),
                ('max_discount', models.IntegerField(default=0, verbose_name='Maximum')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('creat_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='Product Name')),
                ('price', models.IntegerField(null=True, verbose_name='Price')),
                ('view', models.IntegerField(default=0, verbose_name='View')),
                ('sale', models.IntegerField(default=0, verbose_name='Sale')),
                ('material', models.CharField(max_length=50, null=True, verbose_name='Material')),
                ('features', models.CharField(max_length=500, null=True, verbose_name='Features')),
                ('specialized_features', models.CharField(max_length=500, null=True, verbose_name='Specialized Features')),
                ('score', models.FloatField(default=0, verbose_name='Score')),
                ('short_detail', models.CharField(max_length=500, verbose_name='Short Detail')),
                ('detail', models.CharField(max_length=2000, verbose_name='Detail')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brands', to='product.brand', verbose_name='Brand Name')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='product.category', verbose_name='Category')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.discount', verbose_name='Discount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('creat_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('size', models.IntegerField(verbose_name='Size')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('delete_timestamp', models.DateTimeField(blank=True, null=True)),
                ('creat_timestamp', models.DateTimeField(auto_now_add=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(default='/product/default.jpg', upload_to='product', verbose_name='Image')),
                ('main', models.BooleanField(default=False)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product', verbose_name='Product')),
            ],
            options={
                'ordering': ('-update_timestamp',),
            },
        ),
    ]
