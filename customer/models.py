from django.utils.translation import gettext as _

from django.db import models

# Create your models here.
from core.models import User, BaseModel


class Customer(User, BaseModel):
    phone = models.CharField(max_length=11, verbose_name=_('Phone'), unique=True)

    def get_pending_order(self):
        pending_order = self.orders.filter(status='PE')
        return pending_order if pending_order else False

class Address(BaseModel):
    title = models.CharField(max_length=50,verbose_name=_('Title'),default='My address')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    state = models.CharField(max_length=50, verbose_name=_('State'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    no = models.CharField(max_length=50, verbose_name=_('No'))
    postal_code = models.CharField(max_length=10, verbose_name=_('Postal code'))
    address = models.CharField(max_length=500, verbose_name=_('Address'))
