from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.contrib.sites.models import Site

from profiles.models import UserProfile
from expenses.models import Expense, OrderLineItem

import stripe
import os

stripe_public_key = os.environ["STRIPE_PUBLIC_KEY"]
stripe_secret_key = os.environ["STRIPE_SECRET_KEY"]
stripe.api_key = stripe_secret_key


@login_required
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

    if request.method == "GET":
        if "expense_id" in request.GET:
            expense = get_object_or_404(
                Expense, pk=request.GET['expense_id'])
            destination = stripe.Account.retrieve(
                expense.user_profile.stripe_customer_id)
            customer = stripe.Account.retrieve(
                profile.stripe_customer_id)
            order_total = 0
            line_items_array = []
            line_items_ids = {}

            line_items = OrderLineItem.objects.filter(
                user_profile=profile, order=expense, is_paid=False)

            for line_item in line_items:
                line_items_ids.update({line_item.description: line_item.pk})
                order_total += int(line_item.amount * 100)
                price_data = stripe.Price.create(
                    unit_amount=int(line_item.amount * 100),
                    currency="gbp",
                    product_data={
                        'name': line_item.description
                    },
                )

                line_items_array.append({
                    'price': price_data,
                    'quantity': 1,
                })

            session = stripe.checkout.Session.create(
                customer_email=profile.user.email,
                line_items=line_items_array,
                payment_intent_data={
                    'application_fee_amount': round(20 + (order_total * 0.03)),
                    'transfer_data': {
                        'destination': destination,
                    },
                },
                metadata={
                    'destination_profile': expense.user_profile,
                    'expense_id': expense.expense_id,
                    **line_items_ids,
                },
                mode='payment',
                success_url='https://8000-nicobrown-milestone4-2zd8u4fa9x3.ws-eu82.gitpod.io/checkout/checkout_success/{CHECKOUT_SESSION_ID}',
                cancel_url='https://8000-nicobrown-milestone4-2zd8u4fa9x3.ws-eu82.gitpod.io/user_home',
            )

            return redirect(session.url)

    else:
        return redirect('user_home')


@login_required
def checkout_success(request, CHECKOUT_SESSION_ID):
    """
    Handle successful checkouts
    """

    response = stripe.checkout.Session.retrieve(
        CHECKOUT_SESSION_ID,
    )

    if response['payment_status'] == 'paid':
        expense_id = response['metadata']['expense_id']
        expense = Expense.objects.get(expense_id=expense_id)
        print(response)
        destination_profile = UserProfile.objects.get(
            user__username={response['metadata']['destination_profile']})

        line_item_pks = [v for k, v in response['metadata'].items()
                         if v.isnumeric()]
        if line_item_pks:
            for item_pk in line_item_pks:
                line_item = OrderLineItem.objects.get(pk=item_pk)

                if line_item:
                    line_item.is_paid = True
                    line_item.save()
        expense.update_totals()
        expense.save()
        messages.success(
            request,
            f"Payment successfully made to {response['metadata']['destination_profile']}! You may have to wait for the order to process so refresh the page in a few minutes",
            extra_tags=destination_profile.profile_image_url)
    else:
        messages.ERROR(
            request, f"No payment has been made, please try to checkout again")
    return redirect("user_home")
