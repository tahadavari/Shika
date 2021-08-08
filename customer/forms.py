from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from customer.models import Customer


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=11, label=_("Phone"),
                            strip=False, )

    class Meta:
        model = Customer
        fields = ('username', 'email','phone', 'password1', 'password2',)

