from django.contrib import admin

# Register your models here.
from product.models import *
from django.db.models import Q


class SizeInline(admin.StackedInline):
    model = Size
    fields = ['size', 'quantity']
    extra = 1


class ImageInline(admin.StackedInline):
    model = ProductImage
    fields = ['image', 'main']
    extra = 1




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SizeInline, ImageInline]
    list_display = ('name', 'price', 'final_price', 'sale', 'availability','availability_product')
    list_filter = ('brand','category')

    def availability(self, obj):
        return obj.availability_product() > 0

    availability.boolean = True


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')


@admin.register(Discount)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'amount', 'max_discount', 'type')
    list_filter = ('type',)


admin.site.register([Brand])
