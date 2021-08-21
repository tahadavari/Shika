from django.db import models

# Create your models here.
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _

from customer.models import Customer, Address
from product.models import Product, Size


class Order(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'), related_name='orders')
    total_amount = models.IntegerField(verbose_name=_('Total Amount'), default=0)
    address = models.ForeignKey(Address, verbose_name=_('Address'), on_delete=models.CASCADE, related_name='orders',
                                default=None, null=True)
    status = models.CharField(
        choices=[('CA', _('Canceled')),
                 ('PE', _('Pending')),
                 ('CO', _('Completed')),
                 ], verbose_name=_('Status'), max_length=20)

    def calculate_total_finaly(self):
        finaly_total = 0
        for item in self.items.all():
            finaly_total += (item.product.final_price() * item.quantity)
        return finaly_total

    def calculate_total(self):
        total = 0
        for item in self.items.all():
            total += (item.product.price * item.quantity)
        return total

    def get_count(self):
        return self.items.count()

    def get_products_id(self):
        products_id = []
        for item in self.items.all():
            products_id.append(item.product.id)
        return products_id


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('Order'), related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=_('Size'))
    quantity = models.IntegerField(verbose_name=_('Quantity'))
    total = models.IntegerField(verbose_name=_('Total'))

    def __str__(self):
        return f'{self.product.name} :  {self.quantity} : '
