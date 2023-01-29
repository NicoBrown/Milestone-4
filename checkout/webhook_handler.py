from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Checkout_transaction
from expenses.models import Expense, OrderLineItem
from profiles.models import UserProfile

import json
import time
import stripe

# Code below taken from Code institutes Boutique Ado project and adapted


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id

        destination_profile = intent.metadata.destination_profile
        expense_id: intent.metadata.expense_id

        expense_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                expense = Expense.objects.get(
                    expense_id=expense_id,
                    stripe_pid=pid,
                )
                expense_exists = True
                break
            except Expense.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if expense_exists:
            line_items = OrderLineItem.objects.filter(
                user_profile=profile, order=expense)
            if line_items:
                for line_item in line_items:
                    line_item = OrderLineItem.objects.get(pk=int(item_pk))
                    line_item.is_paid = True
                    line_item.save()

            expense.update_totals()
            expense.save()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
