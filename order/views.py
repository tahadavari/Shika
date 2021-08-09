from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from customer.models import Customer
from order.models import OrderItem, Order
from product.models import Product


@csrf_exempt
def add_to_cart(request):
    product_cart = {}
    product_cart[request.POST['id']] = {
        'name': request.POST['name'],
        'quantity': request.POST['quantity'],
        'size': request.POST['size'],
        'price': request.POST['price'],
        'final_price': request.POST['final_price'],
        'main_image': request.POST['main_image']
    }
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

    return JsonResponse({'data': request.session['cart_data'], 'total_item': len(request.session['cart_data'])})


def product_card(request):
    return render(request, 'product_card.html')


@csrf_exempt
def cart_quantity(request):
    if 'cart_data' in request.session:
        return JsonResponse({'total_item': len(request.session['cart_data'])})
    else:
        return JsonResponse({'total_item': 0})


def cart(request):
    total_final_amount = 0
    for p_id, item in request.session['cart_data'].items():
        total_final_amount += int(item['quantity']) * int(item['final_price'])

    total_amount = 0
    for p_id, item in request.session['cart_data'].items():
        if item['price']:
            total_amount += int(item['quantity']) * int(item['price'])
        else:
            total_amount += int(item['quantity']) * int(item['final_price'])

    return render(request, 'cart.html',
                  {'cart_data': request.session['cart_data'], 'total_item': len(request.session['cart_data']),
                   'total_amount': total_amount, 'total_final_amount': total_final_amount})


@csrf_exempt
def delete_from_cart(request):
    p_id = str(request.POST['id'])
    if "cart_data" in request.session:
        if p_id in request.session['cart_data']:
            cart_data = request.session['cart_data']
            del request.session['cart_data'][p_id]
            request.session['cart_data'] = cart_data

    total_final_amount = 0
    for p_id, item in request.session['cart_data'].items():
        total_final_amount += int(item['quantity']) * int(item['final_price'])

    total_amount = 0
    for p_id, item in request.session['cart_data'].items():
        if item['price']:
            total_amount += int(item['quantity']) * int(item['price'])
        else:
            total_amount += int(item['quantity']) * int(item['final_price'])
    t = render_to_string('ajax/cart-list.html',
                         {'cart_data': request.session['cart_data'], 'total_item': len(request.session['cart_data']),
                          'total_amount': total_amount, 'total_final_amount': total_final_amount})
    return JsonResponse({'data': t, 'total_item': len(request.session['cart_data'])})


@csrf_exempt
def update_to_cart(request):
    p_id = str(request.POST['id'])
    p_quantity = request.POST['quantity']
    if 'cart_data' in request.session:
        if p_id in request.session['cart_data']:
            cart_data = request.session['cart_data']
            cart_data[str(request.POST['id'])]['quantity'] = p_quantity
            request.session['cart_data'] = cart_data
            print(request.session['cart_data'])
    total_final_amount = 0
    for p_id, item in request.session['cart_data'].items():
        total_final_amount += int(item['quantity']) * int(item['final_price'])

    total_amount = 0
    for p_id, item in request.session['cart_data'].items():
        if item['price']:
            total_amount += int(item['quantity']) * int(item['price'])
        else:
            total_amount += int(item['quantity']) * int(item['final_price'])
    t = render_to_string('ajax/cart-list.html',
                         {'cart_data': request.session['cart_data'], 'total_item': len(request.session['cart_data']),
                          'total_amount': total_amount, 'total_final_amount': total_final_amount})
    return JsonResponse({'data': t})


@login_required
def check_out(request):
    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty']) * float(item['price'])
        # Order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt
        )
        # End
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty']) * float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-' + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty']) * float(item['price'])
            )
        # End
        # Process Payment
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt,
            'item_name': 'OrderNo-' + str(order.id),
            'invoice': 'INV-' + str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address = UserAddressBook.objects.filter(user=request.user, status=True).first()
        return render(request, 'checkout.html',
                      {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                       'total_amt': total_amt, 'form': form, 'address': address})
