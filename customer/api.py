from rest_framework import generics, renderers, status, mixins
# Create your views here.
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import HttpResponse, render, get_object_or_404, \
    get_list_or_404, redirect
from django.http import JsonResponse

from cart.cart import session_to_cart
from customer.forms import RegisterForm
from customer.serializers import CustomerListSerializer, CustomerDetailSerializer, AddressDetailSerializer, \
    AddressListSerializer
from customer.models import Customer, Address
from customer.permissions import IsSuperUser, IsOwner, permissions
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


class CustomerListApiView(generics.ListAPIView):
    serializer_class = CustomerListSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsSuperUser
    ]


class CustomerDetailApiView(generics.ListAPIView):
    serializer_class = CustomerDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Customer.objects.filter(id=self.request.user.id)



