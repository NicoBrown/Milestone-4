#from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class profiles(models.Model):
    """
    A user profile model for each user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
