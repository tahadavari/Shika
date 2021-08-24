from django.contrib import admin

# Register your models here.
from customer.models import Customer, Address


# class AddressInline(admin.StackedInline):
#     model = Address
#     fields = ['title', 'state', 'city', 'no', 'postal_code', 'address']
#     extra = 1


# @admin.register(Customer)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [AddressInline]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("username", "last_name", "first_name")
