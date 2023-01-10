from django.contrib import admin

# Register your models here.
from .models import Expense, OrderLineItem


class OrderInline(admin.StackedInline):
    model = OrderLineItem


class ExpenseAdmin(admin.ModelAdmin):
    model = Expense
    inlines = [OrderInline]


admin.site.register(Expense, ExpenseAdmin)
