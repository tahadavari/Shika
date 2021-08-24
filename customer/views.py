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
from customer.permissions import IsSuperUser, IsOwner
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


@login_required
@api_view(['GET'])
def address_view(request):
    if request.method == 'GET':
        serializer = AddressListSerializer(Address.objects.filter(customer=request.user), many=True)
        html = render_to_string(template_name='profile/addresses.html', context={'data': serializer.data})
        return JsonResponse({'data': serializer.data, 'html': html})


@login_required
@api_view(['DELETE'])
def address_delete(request, pk):
    try:
        address = Address.objects.get(id=pk)
        print(address)
    except Address.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        operation = address.delete()
        data = {}
        if operation:
            data = {'success': 'Delete address done'}
        else:
            data = {'failed': 'ERROR'}

        return JsonResponse(data)


@login_required
@api_view(['GET', 'POST'])
def address_new(request):
    if request.method == 'GET':
        html = render_to_string(template_name='profile/new_address.html')
        return JsonResponse({'html': html})
    if request.method == 'POST':
        data = {}
        address = AddressDetailSerializer(data=request.data)
        if address.is_valid():
            print(address)
            address.save()
            data = {'success': 'Done'}
        else:
            data = {'failed': 'ERROR'}

        return JsonResponse(data)

@login_required
@api_view(['POST'])
def address_new_cart(request):
    if request.method == 'POST':
        data = {}
        address = AddressDetailSerializer(data=request.data)
        if address.is_valid():
            print(address)
            address.save()
            data = {'success': 'Done'}
        else:
            data = {'failed': 'ERROR'}

        html = render_to_string('ajax/cart-list.html', context={'request': request})
        return JsonResponse({'data': data, 'html': html})

@login_required
@api_view(['GET', 'PUT'])
def address_update(request, pk):
    if request.method == 'GET':
        address = AddressDetailSerializer(Address.objects.get(id=pk))
        html = render_to_string(template_name='profile/edit_address.html', context={'data': address.data})
        return JsonResponse({'html': html})
    if request.method == 'PUT':
        data = {}
        address_old = Address.objects.get(id=pk)
        address = AddressDetailSerializer(address_old, data=request.data)
        if address.is_valid():
            print(address)
            address.save()
            data = {'success': 'Done'}
        else:
            data = {'failed': 'ERROR'}
        return JsonResponse(data)


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
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        user = authenticate(username=username, password=password, phone=phone, email=email, first_name=first_name,
                            last_name=last_name)
        login(request, user)
        return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile/profile.html')


@login_required
@api_view(['GET', 'PUT'])
def personal_information(request):
    if request.method == 'GET':
        html = render_to_string(template_name='profile/personal_information.html',
                                context={'customer': request.customer, 'user': request.user})
        return JsonResponse({'html': html})
    elif request.method == 'PUT':
        data = {}
        customer_old = Customer.objects.get(id=request.customer.id)
        customer = CustomerDetailSerializer(customer_old, data=request.data)
        if customer.is_valid():
            customer.save()
            data = {'success': 'Done'}
        else:
            print(customer.errors)
            data = {'failed': 'ERROR'}
        return JsonResponse(data)


@login_required
@api_view(['GET', 'PUT'])
def change_password(request):
    if request.method == 'GET':
        html = render_to_string(template_name='profile/change-password.html',
                                context={'customer': request.customer, 'user': request.user})
        return JsonResponse({'html': html})
    elif request.method == 'PUT':
        data = {'success': 'Done'}
        customer = Customer.objects.get(id=request.customer.id)
        customer.set_password(request.data['password'])
        customer.save()
        logout(request)
        return JsonResponse(data)

