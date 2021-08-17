from django.utils.translation import gettext_lazy as _

from django.db import models

# Create your models here.
from core.models import User, BaseModel
from customer.validations import phone_validation


class Customer(User):
    phone = models.CharField(max_length=11, verbose_name=_('Phone'), unique=True,validators=[phone_validation])

    def get_pending_order(self):
        if self.orders.filter(status='PE'):
            pending_order = self.orders.filter(status='PE')[0]
            return pending_order
        return None


class Address(BaseModel):
    title = models.CharField(max_length=50, verbose_name=_('Title'), default='My address')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'),
                                 related_name='addresses')
    state = models.CharField(max_length=50, verbose_name=_('State'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    no = models.CharField(max_length=50, verbose_name=_('No'))
    postal_code = models.CharField(max_length=10, verbose_name=_('Postal code'))
    address = models.CharField(max_length=500, verbose_name=_('Address'))

    def __str__(self):
        return f'{self.title} : {self.state} - {self.city} :: {self.address}'
