from django.urls import path

from customer.views import Login, register, logout_user, profile, \
    address_view, address_delete, address_new, address_update, personal_information, change_password

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name="register"),
    path('logout/', logout_user, name="logout"),
    path('address-view/', address_view, name='address_view'),
    path('address-delete/<int:pk>', address_delete, name='address_delete'),
    path('address-new/', address_new, name='address_new'),
    path('address-update/<int:pk>', address_update, name='address_update'),
    path('personal-informatin/', personal_information, name='personal_information'),
    path('change-password/', change_password, name='change_password'),
    path('profile/', profile, name='profile')
]
