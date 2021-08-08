from django.urls import path

from product.views import product_detail, CategoryListAPI, ProductList, all_product, BrandListAPI, SizeList

urlpatterns = [
    path('<int:pk>/', product_detail, name='product_detail'),
    # path('',ProductListApi,name='productlist')
    path('test', ProductList.as_view()),
    path('', all_product),
    path('categorylist', CategoryListAPI.as_view(), name='category_list_api'),
    path('brandlist', BrandListAPI.as_view(), name='brand_list_api'),
    path('size', SizeList.as_view(), name='size_list_api')
]
