from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from product.models import Category, Product, ProductImage


def home(requests):
    parent_category = Category.objects.filter(parent=None)
    child_category = Category.objects.filter(~Q(parent=None))
    top_new: ProductImage = ProductImage.objects.filter(main=True)[:4]
    top_sales: ProductImage = ProductImage.objects.order_by('-product_id__sale').filter(main=True)[:4]
    return render(requests, 'home.html', context={'parent_category': parent_category, 'child_category': child_category,
                                                  'top_new': top_new,'top_sales':top_sales})
