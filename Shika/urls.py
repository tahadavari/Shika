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

import customer.urls
import order.urls
import product.urls
from Shika import settings

from core.views import home
from order.views import cart
from product.views import product_api, ProductList, ProductDetail, category

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', home, name='home'),
                  path('api/', product_api),
                  path('product/', include(product.urls)),
                  path('', include(customer.urls)),
                  path('order/', include(order.urls)),
                  path('productlist/', ProductList.as_view()),
                  path('productdetail/<int:pk>', ProductDetail.as_view()),
                  path('cart', cart, name='cart'),
                  path('shop/<str:pk>', category, name='category'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
