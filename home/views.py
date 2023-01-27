from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from expenses.models import Expense, OrderLineItem
from django.db.models import Q
from django.contrib.auth.models import User
from custom_storages import MediaStorage
from home.forms import Image_form
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import Contact_form

import os
import stripe


# Create your views here.


def index(request):
    """ A view to return the index page """
    contact_form = Contact_form()
    return render(request, 'home/index.html', context={'form': contact_form})


@login_required
def user_home(request):
    """ Display the user's home page. context handled by middleware """

    return render(request, 'home/user_home.html')


@ login_required
def onboard_user(request):

    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    account_response = stripe.Account.retrieve(
        request.profile.stripe_customer_id)

    if account_response.requirements['currently_due'] != []:
        request.profile.stripe_requirements_due = True
        request.profile.save()

        if 'DEVELOPMENT' in os.environ:
            refresh_url = 'https://{request.META["HTTP_X_FORWARDED_HOST"]}/user_home',
            return_url = 'https://{request.META["HTTP_X_FORWARDED_HOST"]}/onboard_user',
        else:
            refresh_url = 'https://kwik-split.herokuapp.com/user_home'
            return_url = 'https://kwik-split.herokuapp.com/onboard_user'

        response = stripe.AccountLink.create(
            account=account_response.id,
            refresh_url=refresh_url,
            return_url=return_url,
            type="account_onboarding",
            collect="eventually_due",
        )
        return redirect(response.url)

    else:
        request.profile.stripe_requirements_due = False
        request.profile.save()

        return redirect(reverse("user_home"))


def contact_form(request):
    """ Display the user's home page. """

    if request.method == "POST":
        form = Contact_form(request.POST, {})
        if form.is_valid():
            subject = 'contact form submission'
            body = form.cleaned_data['message']

            send_mail(
                subject,
                body,
                {os.environ['EMAIL_HOST_USER'], },
                {os.environ['EMAIL_HOST_USER'], }
            )
            messages.info(request, 'Thanks for contacting us!')
            return render(request, 'home/index.html')
        else:
            return render(request, 'home/index.html', context={'form': form})
