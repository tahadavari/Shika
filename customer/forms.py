from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from customer.models import Customer


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=11, label="Phone",
                            strip=False, )
    first_name = forms.CharField(max_length=50, label="First name")
    last_name = forms.CharField(max_length=50, label="Last name")

    class Meta:
        model = Customer
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2',)
