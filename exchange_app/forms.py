from django import forms
from django.contrib.auth.models import User
from exchange_app.models import UserProfileInfo, Order


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_type', 'side', 'price', 'quantity')

            
        