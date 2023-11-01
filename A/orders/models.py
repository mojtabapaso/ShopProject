from django.db import models
from django.contrib.auth import get_user_model
from products.models import Products

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='cart_user')
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity}تا{self.item.title}"

    def price_item(self):
        price = self.item.price * self.quantity
        return price

    class Meta:
        verbose_name_plural = "سبد خرید"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نام کاربر')
    items = models.ManyToManyField(Cart, verbose_name='محصولات')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    ordered_date = models.DateTimeField(verbose_name='تاریخ سفارش', null=True, blank=True)
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name='آدرس')
    ordered = models.BooleanField(default=False, verbose_name='سفارش داده شده است')
    all_price = models.IntegerField(verbose_name='کل ارزش خرید بدون تخفیف', null=True, blank=True)
    price_pey = models.IntegerField(verbose_name='کل مبلغ پرداخت شده', null=True, blank=True)
    price_coupon = models.IntegerField(verbose_name='مبلغ کد تخفیف', null=True, blank=True)

    # --------------
    __original_price = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_price = self.all_price

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.all_price != self.__original_price:
            self.price_pey = None
            self.price_coupon = None
        super().save(force_insert, force_update, *args, **kwargs)

        self.__original_price = self.all_price

    def total(self):
        item = self.items.all()
        var = 0
        for i in item:
            var += i.item.price * i.quantity
        return var

    def pay(self):
        if self.price_coupon:
            return self.all_price - self.price_coupon
        else:
            return self.all_price

    def __str__(self):
        return f"{self.user.phone_number}"


    class Meta:
        verbose_name_plural = "سفارش"


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='related_in_coupon')
    code = models.CharField(max_length=15, null=True, blank=True, help_text="Auto Dont Need To Add")
    amount = models.IntegerField(verbose_name='مقدار', null=True, blank=True)
    min_order = models.IntegerField(verbose_name='حداقل سفارش ', null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='فعال')
    create = models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')
    expiry = models.jDateTimeField(auto_now=True, verbose_name='تاریخ انتضا')

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کد تخفیف ها '
