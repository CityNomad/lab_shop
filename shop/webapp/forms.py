from django import forms
from webapp.models import Item, Order
from django.forms import widgets


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ["name", "description", "category", "balance", 'price']
        widgets = {
            "description": widgets.Textarea(attrs={"placeholder": "enter description"}),
            "category": widgets.RadioSelect,
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["username", "phonenumber", "address"]
        widgets = {
            "address": widgets.Textarea(attrs={"placeholder": "enter address"})
        }


class AddToBasketForm(forms.Form):
    qty = forms.IntegerField(label="Choose amount:")