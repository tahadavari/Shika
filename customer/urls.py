from django.urls import path

from customer.views import Login, register, logout_user

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('register/', register, name="register"),
    path('logout/', logout_user, name="logout"),
    # path('logout/',logout)
]
