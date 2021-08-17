import re

from rest_framework.exceptions import ValidationError


def phone_validation(phone):
    pattern = r'(^09\d{9}$)|(^\+989\d{9}$)'
    if not bool(re.match(pattern,phone)):
        raise ValidationError('phone number wrong')
