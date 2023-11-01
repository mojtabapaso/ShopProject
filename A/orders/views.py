import json

import requests
from A.settings import MERCHANT, description, ZP_API_VERIFY, ZP_API_STARTPAY, ZP_API_REQUEST, CallbackURL
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from permissions import AddressIsNotNone, CartIsNotNone

from .forms import ApplyCouponForm
from .models import Coupon, Order, Cart
from .services import calculate_discounted_price, get_order_by_id, update_items_quantity, complete_order, \
    calculate_total_price

User = get_user_model()




class OrderSummaryView(LoginRequiredMixin, View):
    """ for show information cart
    if user input a code coupon in form
    validate  and true apply
    """

    templates_class = 'orders/summary.html'

    def get(self, request):
        cart = Cart.objects.filter(user=request.user, ordered=False)
        if cart:
            total_price = calculate_total_price(cart)
            return render(request, self.templates_class, {'cart': cart, 'total_price': total_price})
        return render(request, self.templates_class)


class OrderView(LoginRequiredMixin, AddressIsNotNone, CartIsNotNone, View):
    template_name = 'orders/receipt_coupon.html'
    form_class = ApplyCouponForm

    def setup(self, request, *args, **kwargs):
        self.order = Order.objects.get(user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'order': self.order})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            coupon = form.cleaned_data['coupon']
            try:
                amount = request.user.related_in_coupon.get(code=coupon, is_active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'کد تخفیف معتبر نیست', 'danger')
                return redirect('orders:order_item')

            if self.order.all_price < amount.min_order:
                messages.info(request, f'حداقل مقدار خرید برای کد تخفیف {amount.min_order} میباشد', 'info')
                return redirect('orders:order_item')

            discounted_price = calculate_discounted_price(self.order.all_price, amount.amount)
            self.order.price_pey = discounted_price
            self.order.price_coupon = amount.amount
            self.order.save()

            messages.success(request,
                             f'کد تخفیف با موفقیت اعمال شد. مبلغ {amount.amount} کاهش یافت و مبلغ قابل پرداخت {discounted_price} می باشد',
                             'success')
            return redirect('orders:order_item')

        messages.error(request, 'فرم نامعتبر است', 'danger')
        return redirect('orders:order_item')


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_order_by_id(order_id)
        request.session['order_pay'] = {'order_id': order.id}
        amount = order.pay()
        data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user, "email": request.user.profile.email}
        }
        headers = {"accept": "application/json", "content-type": "application/json"}
        response = requests.post(url=ZP_API_REQUEST, data=json.dumps(data), headers=headers)
        response_json = response.json()
        if len(response_json.get('errors', [])) == 0:
            authority = response_json['data']['authority']
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            error = response_json['errors']
            return HttpResponse(f"Error code: {error['code']}, Error Message: {error['message']}")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']
        order = get_order_by_id(order_id)
        update_items_quantity(order)
        complete_order(order)

        status = request.GET.get('Status')
        authority = request.GET['Authority']
        if status == 'OK':
            data = {
                "merchant_id": MERCHANT,
                "amount": order.total(),
                "authority": authority
            }
            headers = {"accept": "application/json", "content-type": "application/json"}
            response = requests.post(url=ZP_API_VERIFY, data=json.dumps(data), headers=headers)
            response_json = response.json()
            if len(response_json.get('errors', [])) == 0:
                t_status = response_json['data']['code']
                if t_status == 100:
                    return HttpResponse('Transaction success.\nRefID: ' + str(response_json['data']['ref_id']))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(response_json['data']['message']))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(response_json['data']['message']))
            else:
                error = response_json['errors']
                return HttpResponse(f"Error code: {error['code']}, Error Message: {error['message']}")
        else:
            return HttpResponse('Transaction failed or canceled by user')
