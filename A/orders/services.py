import datetime

from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from permissions import requires_address
from products.models import Products

from .models import Order, Cart
import logging

from django.utils import timezone


local_time = timezone.localtime(timezone.now())
logger = logging.getLogger(__name__)


def calculate_discounted_price(original_price, discount_amount):
    discounted_price = original_price - discount_amount
    if discounted_price < 0:
        return 0
    return discounted_price


@login_required
@requires_address
def create_order(request):
    cart = Cart.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    order, create = Order.objects.get_or_create(user=request.user)
    order.items.set(cart)
    order.address = profile.address
    order.all_price = order.total()
    order.save()
    return redirect('orders:order_item')


@login_required
def add_to_cart(request, product_slug):
    """add selected product to the cart"""
    product = get_object_or_404(Products, slug=product_slug)
    cart, create = Cart.objects.get_or_create(user=request.user, item=product)

    cart.quantity += 1
    if product.quantity >= cart.quantity:
        # check value quantity is exits
        cart.save()
        messages.success(request, " سبد خرید ویرایش شد.", 'info')
        return redirect('orders:summary_cart')
    else:
        messages.warning(request, 'حداکثر سفارش این محصول به انتها رسیده است', 'danger')
        return redirect('orders:summary_cart')


@login_required
def remove_from_cart(request, product_slug):
    """clear cart from selected product"""
    product = get_object_or_404(Products, slug=product_slug)
    Cart.objects.filter(user=request.user, item=product).delete()
    messages.success(request, "سبد خرید شما پاک شد.", "danger")
    return redirect('orders:summary_cart')


@login_required
def remove_one_cart(request, product_slug):
    # remove one selected product from cart
    product = get_object_or_404(Products, slug=product_slug)
    cart = Cart.objects.get(user=request.user, item=product)
    if cart.quantity == 1:
        # check if quantity product is 1 ,delete a product from cart and show another message
        Cart.objects.filter(user=request.user, item=product).delete()
        messages.success(request, "سبد خرید شما پاک شد.", "danger")
        return redirect('orders:summary_cart')
    cart.quantity -= 1
    cart.save()
    messages.success(request, " سبد خرید ویرایش شد.", "warning")
    return redirect('orders:summary_cart')

def calculate_total_price(cart):
    total_price = 0
    for item in cart:
        total_price += item.price_item()
    return total_price

def get_order_by_id(id):
    try:
        order = Order.objects.get(id)
        return order

    except Exception as e:
        logger.error(f"Name : {logger.name}  | Time {local_time}  : Error {e}")
def update_items_quantity(order):
    for item in order.items.all():
        item.item.quantity -= item.quantity
        item.item.save()

def complete_order(order):
    order.ordered = True
    order.ordered_date = datetime.datetime.now()
    order.save()