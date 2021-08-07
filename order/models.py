from django.db import models

# Create your models here.
from core.models import BaseModel
from django.utils.translation import gettext as _

from customer.models import Customer
from product.models import Product


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    status = models.CharField(
        choices=[('CA', _('Canceled')),
                 ('AP', _('Awaiting Payment')),
                 ('CO', _('Completed')),
                 ], verbose_name=_('Status'),max_length=20)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
