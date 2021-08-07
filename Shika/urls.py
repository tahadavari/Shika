"""Shika URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import product.urls
from Shika import settings

from core.views import tail
from customer.views import AddressDetailAPI, AddressListAPI, CustomerDetailAPI, CustomerListAPI
from product.views import product_api, ProductList, ProductDetail

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', tail, name='home'),
                  path('api/', product_api),
                  path('product/', include(product.urls)),
                  path('productlist/', ProductList.as_view()),
                  path('productdetail/<int:pk>', ProductDetail.as_view()),
                  path('customerlist/', CustomerListAPI.as_view()),
                  path('customerdetail/', CustomerDetailAPI.as_view()),
                  path('addresslist/', AddressListAPI.as_view()),
                  path('addressdetail/<int:pk>', AddressDetailAPI.as_view())
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
