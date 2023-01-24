from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from expenses.models import Expense, OrderLineItem
from django.db.models import Q
from django.contrib.auth.models import User
from custom_storages import MediaStorage
from home.forms import Image_form

import os
import stripe


# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


@login_required
def profile(request, user):

    context = {
        'on_profile_page': False,
    }
    return render(request, "home/user_home.html", context)


@login_required
def user_home(request):
    """ Display the user's home page. """
    template = 'home/user_home.html'

    context = {}
    form = Image_form()
    context['Image_form'] = form

    if request.method == 'POST':
        if request.FILES != {}:
            form = image_form({}, request.FILES)
            if form.is_valid():
                image = request.FILES['image']

                file_directory_within_bucket = f"user_upload_files/{request.user.username}"

                # synthesize a full file path; note that we included the filename
                file_path_within_bucket = os.path.join(
                    file_directory_within_bucket,
                    image.name
                )

                media_storage = MediaStorage()
                media_storage.save(file_path_within_bucket, image)
                request.profile.profile_image_url = media_storage.url(
                    file_path_within_bucket)
                request.profile.save()
            else:
                messages.error(request, form.errors.as_text())
                return render(request, template, context)
    return render(request, template, context)


@ login_required
def update_following(request):
    """ Display the user's profile. """
    if request.method == "POST":
        if 'follow' in request.POST:
            search_profile = get_object_or_404(
                UserProfile, pk=request.POST['follow'])
            request.profile.follows.add(search_profile)

        elif 'unfollow' in request.POST:
            search_profile = get_object_or_404(
                UserProfile, pk=request.POST['unfollow'])
            request.profile.follows.remove(search_profile)

        request.profile.save()

        return redirect("user_home")


@ login_required
def user_search(request):

    profiles = UserProfile.objects.all()

    if request.method == 'GET':
        if 'user_search' in request.GET:
            query = request.GET['user_search']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('user_home'))

            queries = Q(user__username__icontains=query) | Q(
                user__first_name__icontains=query)
            profiles_list = profiles.filter(queries)

            if (profiles_list):
                return render(request, 'home/user_home.html', {'search_profiles': profiles_list})
            else:
                messages.error(
                    request, 'Search Failed. Could not find and users.')
                return redirect(reverse("user_home"))


@ login_required
def onboard_user(request):

    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    account_response = stripe.Account.retrieve(
        request.profile.stripe_customer_id)

    if account_response.requirements['currently_due'] != []:
        request.profile.stripe_requirements_due = True
        request.profile.save()
        response = stripe.AccountLink.create(
            account=account_response.id,
            # TODO: change for deployment
            refresh_url=f'https://{request.META["HTTP_X_FORWARDED_HOST"]}/user_home',
            # TODO: change for deployment
            return_url=f'https://{request.META["HTTP_X_FORWARDED_HOST"]}/onboard_user',
            type="account_onboarding",
            collect="eventually_due",
        )
        return redirect(response.url)

    else:
        request.profile.stripe_requirements_due = False
        request.profile.save()

        return redirect(reverse("user_home"))
