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


@csrf_exempt
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
        if request.cart:
            product_cart['order'] = request.cart.id
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
                print(order_item.errors)
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


@csrf_exempt
def update_to_cart(request):
    t = render_to_string('ajax/cart-list.html',
                         {'cart_data': request.session['cart_data'], 'total_item': len(request.session['cart_data']),
                          'total_amount': total_amount, 'total_final_amount': total_final_amount})
    return JsonResponse({'data': t})


@login_required
@api_view(['GET', 'POST'])
@csrf_exempt
@renderer_classes([renderers.TemplateHTMLRenderer, renderers.JSONRenderer])
def check_out(request):
    total_amount = 0
    item_total_amount = 0
    if request.method == 'POST':
        if 'cart_data' in request.session:
            for p_id, item in request.session['cart_data'].items():
                total_amount += int(item['quantity']) * int(item['final_price'])
                print(total_amount)
            # Order
            print(request.POST)
            customer = Customer.objects.get(id=request.user.id)
            address = Address.objects.get(id=int(request.POST['address']))
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
                address=address,
                status='CO'
            )
            order.save()
            # End
            for p_id, item in request.session['cart_data'].items():
                # OrderItems
                product = Product.objects.get(id=int(p_id))
                size = Size.objects.filter(product=product).first()
                size_quantity = size.quantity
                items = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(item['quantity']),
                    total=int(item['quantity']) * int(item['final_price'])
                )
                items.save()
                size.quantity = size_quantity - 1
                size.save()

            serializer = OrderDetailSerializer(Order.objects.get(id=order.id))
            print(serializer.data)
            return render(request, 'checkout.html', context={'data': serializer.data})
    if request.method == 'GET':
        return redirect('home')
