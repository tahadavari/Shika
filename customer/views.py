from rest_framework import generics
# Create your views here.
from customer.forms import RegisterForm
from customer.serializers import CustomerListSerializer, CustomerDetailSerializer, AddressDetailSerializer, \
    AddressListSerializer
from customer.models import Customer, Address
from customer.permissions import IsSuperUser, IsOwner
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


class CustomerListAPI(generics.ListAPIView):
    serializer_class = CustomerListSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsSuperUser
    ]


class CustomerDetailAPI(generics.RetrieveAPIView):
    serializer_class = CustomerDetailSerializer

    def get_object(self):
        return Customer.objects.get(id=self.request.user.id)


class AddressListAPI(generics.ListAPIView):
    serializer_class = AddressListSerializer

    def get_queryset(self):
        return Address.objects.filter(customer=self.request.user)


class AddressDetailAPI(generics.RetrieveAPIView):
    serializer_class = AddressDetailSerializer
    queryset = Address.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'id'
    permissions = [
        IsOwner
    ]


class Login(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


def logout_user(request):
    logout(request)
    return redirect('home')


def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=password, phone=phone, email=email)
        login(request, user)
        return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
