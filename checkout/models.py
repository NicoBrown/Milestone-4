import uuid
import os
import io

from django.db.models import Model, When, Case, Sum
from django.contrib import messages
from django.shortcuts import render
from django.db import models

from profiles.models import UserProfile
from expenses.models import OrderLineItem, Expense


class Checkout_transaction(Model):
    order = models.ForeignKey(Expense, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='transactions')
    user_sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='user_sender')
    user_recipient = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='user_receiver')
    line_items = models.ForeignKey(OrderLineItem, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='checkout_items')
    amount = models.CharField(max_length=254, null=True, blank=True)
    date = models.DateField(auto_now=True)
    paid_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')
