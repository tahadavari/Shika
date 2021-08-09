from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse


# Create your views here.
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


def update_to_cart(request):
    p_id = str(request.GET['id'])
    p_qantity = request.GET['quantity']
    if 'cart_data' in request.session:
        if p_id in request.session['cart_data']:
            cart_data = request.session['cart_data']
            cart_data[str(request.GET['id'])]['quantity'] = p_qantity
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
    return JsonResponse({'data': t})
