from django.contrib import admin

# Register your models here.
from order.models import OrderItem, Order


class InLineOrderItem(admin.StackedInline):
    model = OrderItem
    fields = ['product', 'quantity']
    extra = 1


admin.site.register([Order, OrderItem])
