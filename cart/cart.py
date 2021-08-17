from Shika import settings
from order.models import Order
from order.serializers import OrderItemSerializer


def session_to_cart(request):
    if request.cart and request.session.get(settings.CART_SESSION_ID):
        for product_id, item in request.session[settings.CART_SESSION_ID].items():
            item['order'] = request.cart.id
            order_item = OrderItemSerializer(data=item)
            if order_item.is_valid():
                if not int(product_id) in request.cart.get_products_id():
                    order_item.save()
            else:
                print(order_item.errors)
        del request.session[settings.CART_SESSION_ID]
    elif request.session.get(settings.CART_SESSION_ID):
        order = Order.objects.create(
            customer=request.customer,
            status='PE'
        )
        order.save()
        for product_id, item in request.session[settings.CART_SESSION_ID]:
            item['order'] = order.id
            order_item = OrderItemSerializer(data=item)
            if order_item.is_valid():
                order_item.save()
        del request.session[settings.CART_SESSION_ID]


