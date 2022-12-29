import io
import os
from PIL import Image
from django.shortcuts import render
from django.contrib import messages
from django.db import models
from google.cloud import vision


class Expense(models.Model):
    sku = models.CharField(max_length=254, null=True, blank=True)
    title = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    data = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
