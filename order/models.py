from django.db import models

# Create your models here.
from core.models import BaseModel
from django.utils.translation import gettext as _

from customer.models import Customer
from product.models import Product


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'), related_name='orders')
    total_amount = models.IntegerField(verbose_name=_('Total Amount'))
    status = models.CharField(
        choices=[('CA', _('Canceled')),
                 ('PE', _('Pending')),
                 ('CO', _('Completed')),
                 ], verbose_name=_('Status'), max_length=20)

    def get_item(self, product):
        item = self.items.filter(product=product)
        return item if item else False


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    total = models.IntegerField(verbose_name=_('Total'))
