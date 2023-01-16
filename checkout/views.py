from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.models import Site

from profiles.models import UserProfile
from expenses.models import Expense, OrderLineItem

import stripe
import os


def checkout(request):
    """ User checkout flow for an unpaid expense

    Parameters:
        expense_id: A expense id parameter to load user specific line items

    Returns:
        binary_sum (str): Binary string of the sum of a and b
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profile': profile,
    }

    stripe_public_key = os.environ["STRIPE_PUBLIC_KEY"]
    stripe_secret_key = os.environ["STRIPE_SECRET_KEY"]
    stripe.api_key = stripe_secret_key

    if request.method == "GET":
        if "expense_id" in request.GET:
            expense = get_object_or_404(
                Expense, pk=request.GET['expense_id'])

            order_total = 0

            line_items = OrderLineItem.objects.filter(
                user_profile=profile, order=expense, is_paid=False)
            for line_item in line_items:
                order_total += float(line_item.amount)

            context.update({"expense": expense,
                            'order_total': order_total})

            total = order_total
            stripe_total = round(total * 100)

            # intent = stripe.PaymentIntent.create(
            #     customer=profile.stripe_customer_id,
            #     amount=stripe_total,
            #     currency=settings.STRIPE_CURRENCY,
            # )

            # context.update({
            #     'stripe_public_key': stripe_public_key,
            #     'client_secret': intent.client_secret,
            # })

            return render(request, "checkout/checkout.html", context)
    elif request.method == "POST":
        return render(request, "checkout/checkout.html", context)
