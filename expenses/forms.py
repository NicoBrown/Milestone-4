from django import forms
from .models import Expense, OrderLineItem


class Order_form(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ('description', 'lineitem_total',
                  'tax_amount',
                  'amount', 'is_paid',)


class Expense_form(forms.Form):

    class Meta:
        model = Expense
        fields = ('total_tax_amount', 'is_paid',
                  'supplier_name', 'total_amount',
                  'tip_amount', 'supplier_address', 'supplier_phone',
                  'net_amount')
