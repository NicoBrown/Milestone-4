from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from django.db.models import Q
from django.contrib.auth.models import User


# Create your views here.


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def profile(request, user):

    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'profile': profile,
        'on_profile_page': False,
    }
    return render(request, "home/user_home.html", context)


def user_home(request):
    """ Display the user's home page. """

    profile = get_object_or_404(UserProfile, user=request.user)

    template = 'home/user_home.html'
    context = {
        'profile': profile
    }

    return render(request, template, context)


@ login_required
def user_search(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    profiles = UserProfile.objects.all()
    query = None

    template = 'home/user_home.html'
    context = {
        'profile': profile
    }

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
                    'profile': profile,
                    'profiles': profiles,
                }
                return render(request, template, context)
            else:
                messages.error(
                    request, 'Search Failed. Could not find and users.')
    return render(request, template, context)


@ login_required
def update_following(request,  pk):
    """ Display the user's profile. """

    current_user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        # if not hasattr(request.user, 'profile'):
        #     missing_profile = UserProfile(user=request.user)
        #     missing_profile.save()
        profile = get_object_or_404(
            UserProfile, pk=pk)
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
        return render(request, "home/user_home.html", {"profile": current_user_profile})

    return render(request, "home/user_home.html", {"profile": current_user_profile})
