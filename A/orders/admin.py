from django.contrib import admin

from .action import *
from .models import Order, Cart, Coupon


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('items', 'user', 'address', 'ordered_date', 'ordered', 'all_price', 'price_pey', 'price_coupon')
    readonly_fields = ('items', 'user', 'ordered_date')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "user", 'id', 'user_name', 'ordered')
    search_fields = ('ordered',)

    fieldsets = (
        ('اطلاعات کاربر', {'fields': ("user",)}),
        ('وضعیت سبد خرید', {'fields': ('ordered', 'item', "quantity")}),
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    exclude = ("code ",)
    readonly_fields = ('code',)
    actions = (activer, deactiver)
