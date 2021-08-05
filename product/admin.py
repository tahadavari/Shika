from django.contrib import admin

# Register your models here.
from product.models import *


class SizeInline(admin.StackedInline):
    model = Size
    fields = ['size', 'quantity']
    extra = 1


class ImageInline(admin.StackedInline):
    model = ProductImage
    fields = ['image','main']
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [SizeInline, ImageInline]


admin.site.register([Brand, Category, Discount])
