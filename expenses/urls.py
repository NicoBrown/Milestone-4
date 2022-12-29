from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('expense', views.expense, name='expense'),
    path('add_expense', views.add_image, name='add_image'),
    path('expense_overview', views.add_expense, name='add_expense'),
]
