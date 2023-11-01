from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import Profile
from functools import wraps
from orders.models import Cart


class AddressIsNotNone:
    """
   validate a profile and address them is not None
    """

    def dispatch(self, request, *args, **kwargs):
        if Profile.objects.get(user=request.user).address:

            return super().dispatch(request, *args, **kwargs)
        else:
            messages.success(request, 'لطفا ابتدا آدرس را در پروفایل کامل کنید', 'warning')
            return redirect('accounts:profile')


class CartIsNotNone:
    """
   check a cart and in cart product is not none
    user can`t use URL and see in page!
    """

    def dispatch(self, request, *args, **kwargs):
        if Cart.objects.filter(user=request.user):

            return super().dispatch(request, *args, **kwargs)
        else:
            messages.success(request, 'سبد خرید شما خالی است !', 'danger')
            return redirect('pages:home')


def requires_address(view):
    """ permission for check address in profile user """

    @wraps(view)
    def _view(request, *args, **kwargs):
        if not Profile.objects.get(user=request.user).address:
            messages.success(request, 'لطفا ابتدا آدرس را در پروفایل کامل کنید', 'info')
            return redirect('accounts:profile')
        return view(request, *args, **kwargs)

    return _view
