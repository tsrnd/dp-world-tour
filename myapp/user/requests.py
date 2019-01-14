from django.core import validators
from django import forms

class UserRegister(forms.Form):
    user_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100,validators=[validators.validate_email])
    password = forms.CharField(max_length=100)

class UserGetToken(forms.Form):
    email = forms.CharField(max_length=100,validators=[validators.validate_email])
    password = forms.CharField(max_length=100)