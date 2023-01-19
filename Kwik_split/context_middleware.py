from profiles.models import UserProfile
from django.shortcuts import get_object_or_404
from django.utils.deprecation import MiddlewareMixin


class SimpleMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # This code is executed just before the view is called
        if request.user.is_authenticated:
            if 'profile' not in request:
                request.profile = UserProfile.objects.filter(
                    user=request.user).first()


def profile(request):

    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        return {'profile': profile, }

    return {}
