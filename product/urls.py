from django.urls import path

from order.views import delete_from_cart
from product.views import product_detail, CategoryListAPI, ProductList, all_product, BrandListAPI, SizeList, \
    add_to_cart, cart_quantity, product_card

urlpatterns = [
    path('<int:pk>/', product_detail, name='product_detail'),
    path('productlist', ProductList.as_view(),name='product_list_api'),
    path('', all_product),
    path('categorylist', CategoryListAPI.as_view(), name='category_list_api'),
    path('brandlist', BrandListAPI.as_view(), name='brand_list_api'),
    path('size', SizeList.as_view(), name='size_list_api'),
    path('add-to-cart', add_to_cart, name='add_to_cart'),
    path('delete-from-cart',delete_from_cart,name = 'delete_from_cart'),
    path('cart_quantity', cart_quantity, name='cart_quantity'),

]
