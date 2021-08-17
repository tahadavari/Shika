from django.shortcuts import render
from django.db.models import Q
from Shika import settings
from django.http import JsonResponse

# Create your views here.
from cart.cart import session_to_cart
from product.models import Category, Product, ProductImage


def home(request):
    if request.user.is_authenticated and request.session.get(settings.CART_SESSION_ID):
        session_to_cart(request)
    # print(request.cart.items)
    parent_category = Category.objects.filter(parent=None)
    child_category = Category.objects.filter(~Q(parent=None))
    top_new: ProductImage = ProductImage.objects.filter(main=True)[:4]
    top_sales: ProductImage = ProductImage.objects.order_by('-product_id__sale').filter(main=True)[:4]
    return render(request, 'home.html', context={'parent_category': parent_category, 'child_category': child_category,
                                                 'top_new': top_new, 'top_sales': top_sales})
