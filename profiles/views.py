from django.contrib import messages
from django.urls import path
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User
from custom_storages import MediaStorage
from home.forms import Image_form
from .forms import Profile_edit_form, User_edit_form
from django.db.models import Q
from django.forms.models import model_to_dict
from django.forms import inlineformset_factory

import os


# Create your views here.


@login_required
def profile(request, profile_id):

    render(request, f'/profile/{profile_id}')


@ login_required
def edit_profile(request):

    image_form = Image_form()
    profile_edit_form = Profile_edit_form(instance=request.profile, prefix='profile',
                                          initial=model_to_dict(request.profile))
    user_edit_form = User_edit_form(instance=request.user,
                                    prefix='user', initial=model_to_dict(request.user))

    context = {
        'image_form': image_form,
        'profile_edit_form': profile_edit_form,
        'user_edit_form': user_edit_form,
    }

    if request.method == 'POST':
        if request.FILES != {}:
            form = Image_form({}, request.FILES, )
            if form.is_valid():
                print(form.errors)
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
                return redirect('edit_profile')
            else:
                messages.error(request, form.errors.as_text())
                return render(request, 'profiles/edit_profile.html', context)
        else:
            profile_form = Profile_edit_form(
                request.POST, {}, prefix='profile', instance=request.profile)
            user_form = User_edit_form(
                request.POST, {}, prefix='user', instance=request.user)

            if profile_form.is_valid() and user_form.is_valid():
                profile_form.save()
                user_form.save()
                messages.success(request, "Profile Updated")
            else:
                context['profile_edit_form'] = profile_form
                context['user_edit_form'] = user_form
                messages.error(request, user_form.errors.as_text())
                messages.error(request, profile_form.errors.as_text())

            return redirect('edit_profile')
    else:
        return render(request, "profiles/edit_profile.html", context)


@ login_required
def delete_profile(request, profile_id):
    """ Delete a users profile """

    if request.method == "POST":
        user = User.objects.get(pk=profile_id).first()
        user.delete()

        messages.success(request, 'Account deleted!')
        return redirect(reverse('index'))
    else:
        return redirect('edit_profile', profile_id)


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

        return redirect("edit_profile")


@ login_required
def user_search(request):
    """ Search for users and return the users """

    if request.method == 'GET':
        if 'user_search' in request.GET:
            profiles = UserProfile.objects.all()
            query = request.GET['user_search']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect('edit_profile', profile_id)

            queries = Q(user__username__icontains=query) | Q(
                user__first_name__icontains=query)
            profiles_list = profiles.filter(queries)

            if (profiles_list):
                return render(request, 'profiles/edit_profile.html', {'search_profiles': profiles_list})

            else:
                messages.error(
                    request, 'Search Failed. Could not find and users.')
                return redirect(reverse("edit_profile"))
    else:
        return render(request, "profiles/edit_profile.html")
