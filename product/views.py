from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
from rest_framework.views import APIView

from core.admin import logical_delete
from customer.models import Customer
from product.models import Product, ProductImage, Size, Category, Brand
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins
from product.serializers import ProductDetailSerializer, CategorySerializer, ProductBriefSerializer, BrandSerializer, \
    SizeSerializer


def product_detail(request, pk):
    parent_category = Category.objects.filter(parent=None)
    child_category = Category.objects.filter(~Q(parent=None))
    product = Product.objects.get(id=pk)
    product_image_main = ProductImage.objects.filter(main=True, product_id=product).first()
    product_images = ProductImage.objects.filter(product_id=product)
    product_sizes = Size.objects.filter(product=product)

    return render(request, 'product.html',
                  context={'parent_category': parent_category, 'child_category': child_category, 'product': product,
                           'product_image_main': product_image_main,
                           'product_sizes': product_sizes, 'product_images': product_images})


# ----------------------------------------------------------------------------------------------------------------------

@csrf_exempt
def product_api(request):
    if request.method == 'GET':
        # List of Questions!
        product = Product.objects.all()
        s = ProductDetailSerializer(product, many=True)
        return JsonResponse({
            "products": s.data
        })
    elif request.method == 'POST':
        # Create new instance!
        s = ProductDetailSerializer(data=request.POST)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data)
        else:
            return JsonResponse(s.errors, status=400)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductBriefSerializer


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_url_kwarg = 'pk'
    lookup_field = 'id'


class ProductDetailBrief(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductBriefSerializer
    lookup_url_kwarg = 'pk'
    lookup_field = 'id'


class CategoryListAPI(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


class BrandListAPI(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class SizeList(generics.ListAPIView):
    queryset = Size.objects.all().distinct('quantity')
    serializer_class = SizeSerializer


def all_product(request):
    return render(request, 'shop.html')


def category(request, pk):
    print(Category.objects.get(id=8))
    category_ = Category.objects.get(id=pk)
    print(category_)
    if category_.parent:
        products = Product.objects.filter(category=category_)
    else:
        products = Product.objects.filter(category__parent=category_)

    return render(request, 'shop.html', context={'products': products})
