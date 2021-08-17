from django.urls import path

from order.views import delete_from_cart
from product.views import product_detail, CategoryListAPI, ProductList, all_product, BrandListAPI, SizeList, \
    ProductDetail

urlpatterns = [
    path('<int:pk>/', product_detail, name='product_detail'),
    path('productlist', ProductList.as_view(), name='product_list_api'),
    path('', all_product),
    path('categorylist', CategoryListAPI.as_view(), name='category_list_api'),
    path('brandlist', BrandListAPI.as_view(), name='brand_list_api'),
    path('size', SizeList.as_view(), name='size_list_api'),
    path('papi/<int:pk>', ProductDetail.as_view())

]
