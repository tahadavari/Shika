from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from product.models import Product, ProductImage, Size
from django.views.decorators.csrf import csrf_exempt

from product.serializers import ProductSerializer


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    print(product)
    product_image_main = ProductImage.objects.filter(main=True,product_id=product).first()
    print(product_image_main)
    product_images = ProductImage.objects.filter(product_id=product)
    print(product_images)
    product_sizes = Size.objects.filter(product=product)
    return render(request, 'product.html', context={'product': product, 'product_image_main': product_image_main,
                                                    'product_sizes': product_sizes,'product_images':product_images})


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
