from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from product.models import Category, Product,ProductImage


def tail(requests):
    parent_category = Category.objects.filter(parent=None)
    child_category = Category.objects.filter(~Q(parent=None))
    top_product = Product.objects.all()[:5]
    return render(requests, 'home.html', context={'parent_category': parent_category,'child_category': child_category,'top_product':top_product})
