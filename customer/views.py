from rest_framework import generics
# Create your views here.
from customer.serializers import CustomerListSerializer, CustomerDetailSerializer, AddressDetailSerializer, \
    AddressListSerializer
from customer.models import Customer, Address
from customer.permissions import IsSuperUser, IsOwner


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
