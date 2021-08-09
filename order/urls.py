from django.urls import path

from order.views import delete_from_cart, update_to_cart, add_to_cart, cart_quantity, check_out

urlpatterns = [
    path('add-to-cart', add_to_cart, name='add_to_cart'),
    path('delete-from-cart', delete_from_cart, name='delete_from_cart'),
    path('update-to-cart', update_to_cart, name='update_to_cart'),
    path('cart-quantity', cart_quantity, name='cart_quantity'),
    path('check-out', check_out, name='check_out'),
]
