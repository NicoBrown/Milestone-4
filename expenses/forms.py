from django import forms
from .models import Expense, OrderLineItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ('lineitem_total',
                  'tax_amount', 'is_paid',
                  'order', 'user_profile', 'description', 'amount',
                  'stripe_pid',)


class Expense_form(forms.Form):

    class Meta:
        model = Expense
        fields = ('expense_id',
                  'total_tax_amount', 'is_paid',
                  'supplier_name', 'user_profile', 'paid_amount', 'total_amount',
                  'tip_amount', 'supplier_address', 'supplier_phone'
                  'image_url', 'line_item_count', 'net_amount')
