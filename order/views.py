from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from rest_framework import renderers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response

from Shika import settings
from customer.models import Customer, Address
from order.models import OrderItem, Order
from order.serializers import OrderDetailSerializer, OrderItemSerializer
from product.models import Product, Size


@login_required()
def add_to_cart(request):
    product_cart = {}
    product_cart[request.POST['id']] = {
        'order': request.POST['order'],
        'product': request.POST['id'],
        'quantity': request.POST['quantity'],
        'size': request.POST['size'],
        'total': request.POST['total']
    }
    if request.user.is_authenticated:
        if not request.cart:
            print('if not')
            order = Order.objects.create(
                customer=request.customer,
                status='PE'
            )
            order.save()
            request.cart = order
        product_cart[request.POST['id']]['order'] = request.cart.id
        order_item = OrderItemSerializer(data=product_cart[request.POST['id']])

        if order_item.is_valid():
            if int(request.POST['id']) in request.cart.get_products_id():
                pre_order_item = request.cart.items.get(product_id=int(request.POST['id']))
                pre_order_item.quantity = int(product_cart[request.POST['id']]['quantity'])
                pre_order_item.total = int(product_cart[request.POST['id']]['quantity']) * int(
                    product_cart[request.POST['id']]['total'])
                pre_order_item.save()
                print(pre_order_item.quantity)
            else:
                order_item.save()
        else:
            print('51:', order_item.errors)
        # print(*request.cart.items.all())
        print(request.cart.get_count())
        return JsonResponse({'success': 'done', 'total_item': request.cart.get_count()})
    else:
        if "cart_data" in request.session:
            if str(request.POST['id']) in request.session['cart_data']:
                cart_data = request.session['cart_data']
                cart_data[str(request.POST['id'])]['quantity'] = int(product_cart[str(request.POST['id'])]['quantity'])
                cart_data.update(cart_data)
                request.session['cart_data'] = cart_data
            else:
                cart_data = request.session['cart_data']
                cart_data.update(product_cart)
                request.session['cart_data'] = cart_data
        else:
            request.session['cart_data'] = product_cart
        print(request.session['cart_data'])
        return JsonResponse({'data': request.session['cart_data'], 'total_item': len(request.session['cart_data'])})


def product_card(request):
    return render(request, 'product_card.html')


@csrf_exempt
def cart_quantity(request):
    if 'cart_data' in request.session:
        return JsonResponse({'total_item': len(request.session['cart_data'])})
    else:
        return JsonResponse({'total_item': 0})


@login_required()
def cart(request):
    return render(request, 'cart.html')


@login_required()
def delete_from_cart(request):
    item: OrderItem = request.cart.items.get(id=request.POST['id'])
    item.delete()
    html = render_to_string('ajax/cart-list.html', context={'request': request})
    return JsonResponse({'data': 'done', 'html': html})


@login_required()
def update_to_cart(request):
    if request.method == 'POST':
        order_item = request.cart.items.get(id=int(request.POST['id']))
        order_item.quantity = int(request.POST['quantity'])
        order_item.save()
        html = render_to_string('ajax/cart-list.html', context={'request': request})
        return JsonResponse({'data': 'done', 'html': html})


@login_required
@api_view(['POST'])
def check_out(request):
    if request.method == 'POST':
        order = request.cart

        address = Address.objects.get(id=int(request.POST['address']))
        order.address = address
        order.total_amount = request.cart.calculate_total_finaly()
        order.status = 'CO'

        order.save()
        html = render_to_string('receipt.html', context={'order': order})
        return JsonResponse({'data': 'done', 'html': html})


@login_required
@api_view(['GET'])
def my_order_list(request):
    if request.method == 'GET':
        serializer = OrderDetailSerializer(Order.objects.filter(customer=request.user, status='CO'), many=True)
        html = render_to_string(template_name='profile/my_order.html', context={'data': serializer.data})
        return JsonResponse({'data': serializer.data, 'html': html})


@login_required
@api_view(['GET'])
def my_order_detail(request,pk):
    if request.method == 'GET':
        order = Order.objects.get(id=pk)
        html = render_to_string('profile/order_detail.html', context={'order': order})
        return JsonResponse({'data': 'done', 'html': html})