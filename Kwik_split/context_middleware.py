from profiles.models import UserProfile
from expenses.models import OrderLineItem, Expense
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
        print(request.resolver_match._func_path)

        paid_expenses = []
        unpaid_expenses = []

        if request.path.startswith('/user_home'):
            line_items = OrderLineItem.objects.filter(user_profile=profile)

            for line_item in line_items:
                if line_item.is_paid is True:
                    if line_item.order not in paid_expenses:
                        paid_expenses.append(line_item.order)
                else:
                    if line_item.order not in unpaid_expenses:
                        unpaid_expenses.append(line_item.order)

        return {'profile': profile,
                'unpaid_expenses': unpaid_expenses,
                'paid_expenses': paid_expenses, }

    return {}
