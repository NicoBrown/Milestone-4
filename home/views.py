from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from expenses.models import Expense, OrderLineItem
from django.db.models import Q
from django.contrib.auth.models import User
from custom_storages import MediaStorage

import os


# Create your views here.


def index(request):
    """ A view to return the index page """
    if request.user.is_authenticated:

        profile = get_object_or_404(UserProfile, user=request.user)

        context = {
            'profile': profile,
            'on_profile_page': False,
        }

        return render(request, 'home/index.html', context)
    return render(request, 'home/index.html')


def profile(request, user):

    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)

        context = {
            'profile': profile,
            'on_profile_page': False,
        }
        return render(request, "home/user_home.html", context)

    return render(request, "home/user_home.html", context)


def user_home(request):
    """ Display the user's home page. """
    expense_list = []
    template = 'home/user_home.html'
    profile = get_object_or_404(UserProfile, user=request.user)
    profiles = UserProfile.objects.all()
    query = None

    line_items = OrderLineItem.objects.filter(user_profile=profile)
    for line_item in line_items:
        if line_item.order.user_profile != request.user:
            if line_item.order not in expense_list:
                expense_list.append(line_item.order)

    if request.method == 'GET':
        if 'user_search' in request.GET:
            query = request.GET['user_search']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('user_home'))

            queries = Q(user__username__icontains=query) | Q(
                user__first_name__icontains=query)
            profiles = profiles.filter(queries)
            if (profiles):
                context = {
                    'expenses': expense_list,
                    'profile': profile,
                    'profiles': profiles,
                }
                return render(request, template, context)
            else:
                messages.error(
                    request, 'Search Failed. Could not find and users.')
    if request.method == "POST":
        if request.FILES != {}:
            image = request.FILES['image']

            file_directory_within_bucket = f"user_upload_files/{profile.user.username}"

            # synthesize a full file path; note that we included the filename
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                image.name
            )

            media_storage = MediaStorage()
            media_storage.save(file_path_within_bucket, image)
            profile.profile_image_url = media_storage.url(
                file_path_within_bucket)

        if 'follow' in request.POST:
            search_profile = get_object_or_404(
                UserProfile, pk=request.POST['follow'])
            profile.follows.add(search_profile)
        elif 'unfollow' in request.POST:
            search_profile = get_object_or_404(
                UserProfile, pk=request.POST['unfollow'])
            profile.follows.remove(search_profile)
        profile.save()

    context = {
        'expenses': expense_list,
        'profile': profile
    }

    return render(request, template, context)


@ login_required
def update_following(request,  pk):
    """ Display the user's profile. """

    current_user_profile = get_object_or_404(UserProfile, user=request.user)

    return render(request, "home/user_home.html", {"profile": current_user_profile})
