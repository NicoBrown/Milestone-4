import io
import os
import uuid
from PIL import Image
from django.shortcuts import render
from django.contrib import messages
from django.db import models
from django.db.models import Model, When, Case, Sum

from profiles.models import UserProfile


class Expense(Model):
    expense_id = models.CharField(
        max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='expense')
    supplier_name = models.CharField(max_length=254, null=True, blank=True)
    supplier_address = models.CharField(max_length=254, null=True, blank=True)
    supplier_phone = models.CharField(max_length=254, null=True, blank=True)
    image = models.ImageField(
        null=True, default="image", upload_to='media/user_upload_files/')
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    date = models.DateField(auto_now=True)
    line_item_count = models.IntegerField(null=True, blank=True)
    total_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    total_tax_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    tip_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    net_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    paid_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)

    def update_totals(self):
        """
        Update net amount each time a line item is added,
        accounting for tax and tip costs.
        """
        self.paid_amount = self.lineitems.filter(is_paid=True).aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0
        self.line_item_count = self.lineitems.count()
        if not self.total_amount:
            self.total_amount = self.lineitems.aggregate(Sum('lineitem_total'))[
                'lineitem_total__sum'] or 0
        if not self.net_amount:
            self.net_amount = self.total_amount
            + self.total_tax_amount + self.tip_amount
        self.save()

    def __str__(self):
        return self.expense_id


class OrderLineItem(Model):
    order = models.ForeignKey(Expense, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='lineitems')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='expenses')
    lineitem_total = models.DecimalField(null=True, blank=True,
                                         max_digits=6, decimal_places=2)
    description = models.CharField(max_length=254, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    tax_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)
    stripe_pid = models.CharField(
        max_length=254, null=True, blank=True, default='')

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        if not self.lineitem_total:
            self.lineitem_total = float(
                self.amount) * float(self.quantity)
            if self.tax_amount:
                self.lineitem_total + float(self.tax_amount)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
