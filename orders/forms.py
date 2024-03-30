from django import forms
from orders.models import Order


class Order_form (forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2','city','state','country','order_note']