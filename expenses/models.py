import io
import os
from PIL import Image
from django.shortcuts import render
from django.contrib import messages
from django.db import models


class Expense(models.Model):
    sku = models.CharField(max_length=254, null=True, blank=True)
    supplier_name = models.CharField(max_length=254, null=True)
    description = models.TextField()
    quantity = models.IntegerField(default=1, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    data = models.DateField(auto_now=True)
    total_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    total_tax_amount = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
