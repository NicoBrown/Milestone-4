from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.validators import EmailValidator, RegexValidator

import stripe
import os

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    phone_regex = RegexValidator(
        regex=r'^\w[0-9]{6,15}$', message="Phone number must be numbers only. Up to 20 digits allowed.")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True)
    stripe_customer_id = models.CharField(
        max_length=100, default="", null=True, blank=True)
    stripe_requirements_due = models.BooleanField(default=True)
    default_phone_number = models.CharField(validators=[phone_regex],
                                            max_length=20, null=True, blank=True, default="0")
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
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    user_object = UserProfile.objects.filter(user=instance).first()

    if user_object is None:
        user_profile = UserProfile(user=instance)

        if not user_profile.stripe_customer_id:
            user_account_response = stripe.Account.create(
                email=instance.email,
                country="GB",
                type="custom",
                business_type='individual',
                individual={
                    "first_name": instance.first_name,
                    "last_name": instance.last_name,
                },
                business_profile={"url": "https://www.google.com/",
                                  "mcc": "5734"},
                capabilities={"card_payments": {"requested": True},
                              "transfers": {"requested": True}},
                tos_acceptance={"date": 1609798905, "ip": "0.0.0.0"},
            )
        user_profile.stripe_customer_id = user_account_response.stripe_id
        user_profile.save()
