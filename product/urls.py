from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Shika import settings

from core.views import tail
from product.views import product_api, product_detail

urlpatterns = [
                  path('<int:pk>/', product_detail, name='product_detail')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
