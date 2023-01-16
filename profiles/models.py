from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import stripe
import os

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True)
    stripe_customer_id = models.CharField(
        max_length=20, default="", null=True, blank=True)
    stripe_requirements_due = models.BooleanField(default=True)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country *', null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    profile_image_url = models.URLField(
        max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        user_profile = UserProfile(user=instance)
        stripe.api_key = "sk_test_51MOlcgGL2Yk3bPvdwA0i5CQEQJscrbeoHnctzks8WvTdN0L0pUYsQBYP1kdS7yrPxUPYaEoKTgEATElzy62knLQc00ORjtOIWy"

        user_account_response = stripe.Account.create(
            email=user_profile.user.email,
            country="GB",
            type="custom",
            business_type='individual',
            individual={
                "first_name": user_profile.user.first_name,
                "last_name": user_profile.user.first_name,
            },
            business_profile={"url": "https://www.google.com/",
                              "mcc": "5734"},
            capabilities={"card_payments": {"requested": True},
                          "transfers": {"requested": True}},
            tos_acceptance={"date": 1609798905, "ip": "0.0.0.0"},
        )

        user_profile.stripe_customer_id = user_account_response.stripe_id

        user_profile.save()
    # Existing users: just save the profile
    # instance.UserProfile.save()
