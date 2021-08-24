from django.db import models
# Create your models here.
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse
from django.contrib import admin

from core.models import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('Brand Name'))

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('Category Name'))
    icon = models.ImageField(verbose_name=_('Icon'), upload_to=r'category/icon', default='category/icon/default.png')
    image = models.ImageField(verbose_name=_('Image'), upload_to=r'category/image',
                              default='category/image/default.jpg')
    parent = models.ForeignKey('self', null=True, verbose_name=_('Parent'), on_delete=models.CASCADE, blank=True,
                               related_name='subcategory')

    def __str__(self):
        return self.name

    def get_product_count(self):
        product_sub = len(self.categories.all())
        product_parent = 0
        for i in self.subcategory.all():
            product_parent += len(i.categories.all())
        return product_sub + product_parent

    def get_url(self):
        return reverse('category', args=(self.pk,))


class Discount(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    percent = models.IntegerField(verbose_name=_('Percent'), default=0)
    amount = models.IntegerField(verbose_name=_('Amount'), default=0)
    type = models.CharField(verbose_name=_('Type'), max_length=10, choices=[
        ('PR', 'Percent'),
        ('AM', 'Amount')
    ], default=None, null=True, blank=True)
    max_discount = models.IntegerField(verbose_name=_('Maximum'), default=0)


class Product(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('Product Name'))
    price = models.IntegerField(verbose_name=_('Price'), null=True)
    view = models.IntegerField(verbose_name=_('View'), default=0)
    sale = models.IntegerField(verbose_name=_('Sale'), default=0)
    material = models.CharField(max_length=50, verbose_name=_('Material'), null=True)
    features = models.CharField(max_length=500, verbose_name=_('Features'), null=True)
    specialized_features = models.CharField(max_length=500, verbose_name=_('Specialized Features'), null=True)
    score = models.FloatField(verbose_name=_('Score'), default=0)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, verbose_name=_('Brand Name'), null=True,
                              related_name='brands')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('Category'),
                                 null=True, related_name='categories')
    discount = models.ForeignKey(Discount, null=True, on_delete=models.SET_NULL, verbose_name=_('Discount'), blank=True)
    short_detail = models.CharField(max_length=500, verbose_name=_('Short Detail'))
    detail = models.CharField(max_length=2000, verbose_name=_('Detail'))

    def __str__(self):
        if self.name:
            return str(self.name)
        else:
            return self.brand

    def get_url(self):
        return reverse('product_detail', args=(self.pk,))

    def final_price(self):
        if self.discount:
            if self.discount.type == 'PR':
                dis = round((self.discount.percent * self.price) / 100)
                if self.discount.max_discount:
                    if dis > self.discount.max_discount:
                        return self.price - self.discount.max_discount
                    return self.price - dis
                return self.price - dis
            elif self.discount.type == 'AM':
                return self.price - self.discount.amount
        else:
            return self.price

    def main_image(self):
        return self.images.filter(main=True).first()

    def availability_product(self):
        if len(self.sizes.all().filter(quantity__gt=0)):
            count = 0
            for i in self.sizes.all().filter(quantity__gt=0):
                count += i.quantity
            return count
        else:
            return 0


class ProductImage(BaseModel):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'), related_name='images')
    image = models.ImageField(verbose_name=_('Image'), upload_to='product', default='/product/default.jpg')
    main = models.BooleanField(default=False)

    class Meta:
        ordering = ('-update_timestamp',)

    def __str__(self):
        return self.product_id.name


class Size(BaseModel):
    size = models.IntegerField(verbose_name=_('Size'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')

    def __str__(self):
        return f'{self.product.name} : {self.size}'
