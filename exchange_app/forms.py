from django import forms
from django.contrib.auth.models import User
from exchange_app.models import UserProfileInfo, Order, OrderType


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirmation = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords no match")

        return cleaned_data

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ()

class BalanceForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ()


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type', 'order_side', 'order_price', 'order_quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_price'].required = False

    def clean(self):
        cleaned_data = super().clean()
        order_type = cleaned_data.get('order_type')
        order_price = cleaned_data.get('order_price')
        order_quantity = cleaned_data.get('order_quantity')

        if not order_type or not order_quantity:
            raise forms.ValidationError("Order type and quantity are required.")

        if order_type == OrderType.LIMIT.name:
            if not order_price:
                raise forms.ValidationError("Order price is required for LIMIT orders.")
            if order_price < 0.01 or order_price > 10.00:
                raise forms.ValidationError("Order price must be between 0.01 and 10.00.")

        return cleaned_data