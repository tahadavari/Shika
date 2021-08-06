from django.db import models

# Create your models here.
from django.utils.translation import gettext as _
from rest_framework.reverse import reverse

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
    parent = models.ForeignKey('self', null=True, verbose_name=_('Parent'), on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.name


class Discount(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    percent = models.IntegerField(verbose_name=_('Percent'))
    max_discount = models.IntegerField(verbose_name=_('Maximum'))


def mainimg(self):
    main = ProductImage.objects.filter(product=self, main=True)
    return main


class Product(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('Product Name'))
    price = models.IntegerField(verbose_name=_('Price'), null=True)
    view = models.IntegerField(verbose_name=_('View'), default=0)
    sale = models.IntegerField(verbose_name=_('Sale'), default=0)
    material = models.CharField(max_length=50, verbose_name=_('Material'), null=True)
    features = models.CharField(max_length=500, verbose_name=_('Features'), null=True)
    specialized_features = models.CharField(max_length=500, verbose_name=_('Specialized Features'), null=True)
    score = models.FloatField(verbose_name=_('Score'), default=0)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, verbose_name=_('Brand Name'), null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name=_('Category'),
                                 null=True)
    discount = models.ForeignKey(Discount, null=True, on_delete=models.SET_NULL, verbose_name=_('Discount'), blank=True)
    short_detail = models.CharField(max_length=500, verbose_name=_('Short Detail'))
    detail = models.CharField(max_length=2000, verbose_name=_('Detail'))

    def __str__(self):
        return self.name

    def get_url(self):
        print('pk',self.pk)
        return reverse('product_detail', args=(self.pk,))


class ProductImage(BaseModel):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'), related_name='images')
    image = models.ImageField(verbose_name=_('Image'), upload_to='product', default='/product/default.jpg')
    main = models.BooleanField(default=False)

    class Meta:
        ordering = ('-update_timestamp',)


class Size(BaseModel):
    size = models.IntegerField(verbose_name=_('Size'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} : {self.size}'