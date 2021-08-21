from django.urls import path

from customer.views import Login, register, logout_user, profile, \
    address_view, address_delete, address_new, address_update, personal_information, change_password, address_new_cart
from order.views import my_order_list, my_order_detail

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name="register"),
    path('logout/', logout_user, name="logout"),
    path('address-view/', address_view, name='address_view'),
    path('address-delete/<int:pk>', address_delete, name='address_delete'),
    path('address-new/', address_new, name='address_new'),
    path('address-new-cart/', address_new_cart, name='address_new_cart'),
    path('address-update/<int:pk>', address_update, name='address_update'),
    path('personal-informatin/', personal_information, name='personal_information'),
    path('change-password/', change_password, name='change_password'),
    path('my-order-list/', my_order_list, name='my_order_list'),
    path('my-order-detail/<int:pk>', my_order_detail, name='my_order_detail'),
    path('profile/', profile, name='profile')
]

