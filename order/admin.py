from django.contrib import admin

# Register your models here.
from order.models import OrderItem, Order


class InLineOrderItem(admin.StackedInline):
    model = OrderItem
    fields = ['product', 'quantity']
    extra = 1


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product','size','quantity','total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','customer','total_amount','status')
    list_filter = ('status',)

