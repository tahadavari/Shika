from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView

from core.admin import logical_delete
from product.models import Product, ProductImage, Size
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, mixins
from product.serializers import ProductSerializer


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    product_image_main = ProductImage.objects.filter(main=True, product_id=product).first()
    product_images = ProductImage.objects.filter(product_id=product)
    product_sizes = Size.objects.filter(product=product)
    return render(request, 'product.html', context={'product': product, 'product_image_main': product_image_main,
                                                    'product_sizes': product_sizes, 'product_images': product_images})


# ----------------------------------------------------------------------------------------------------------------------

@csrf_exempt
def product_api(request):
    if request.method == 'GET':
        # List of Questions!
        product = Product.objects.all()
        s = ProductSerializer(product, many=True)
        return JsonResponse({
            "products": s.data
        })
    elif request.method == 'POST':
        # Create new instance!
        s = ProductSerializer(data=request.POST)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data)
        else:
            return JsonResponse(s.errors, status=400)


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.DestroyAPIView, generics.UpdateAPIView,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'pk'
    lookup_field = 'id'

