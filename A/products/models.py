from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_jalali.db import models as jmodels
from pages.models import Category

User = get_user_model()


class Brand(models.Model):
    category = models.ManyToManyField(Category, related_name='brand', verbose_name='دسته بندی')
    name = models.CharField(max_length=150, verbose_name='اسم')
    slug = models.SlugField(max_length=120, blank=True, null=True)

    class Meta:
        verbose_name_plural = "نام تجاری"

    def __str__(self):
        return self.name


class Products(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    price = models.IntegerField(verbose_name='قیمت')
    discount_price = models.IntegerField(blank=True, null=True, verbose_name='درصد تخفیف')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='نام تجاری')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product')
    slug = models.SlugField()
    description = RichTextField(default=' ', verbose_name='توضیحات')
    image = models.ImageField(upload_to='static/img', verbose_name='تصویر')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    quantity = models.PositiveSmallIntegerField(verbose_name='موجودی')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:product_detail', kwargs={'slug': self.slug})

    def get_brand_product(self):
        return reverse('pages:brand_slug', kwargs={'slug': self.brand.slug})

    # def get_add_to_cart_url(self):
    #     return reverse("pages:add-to-cart", kwargs={'slug': self.slug})
    #
    # def get_remove_from_cart_url(self):
    #     return reverse("pages:remove-from-cart", kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = "محصول"


class Commend(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='کاربر')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='محصول')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_commend', null=True, blank=True,
                              verbose_name='پاسخ')
    is_reply = models.BooleanField(default=False, verbose_name='پاسخ است')
    body = RichTextField(verbose_name='بدنه')
    create = jmodels.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')
    active = models.BooleanField(default=False, verbose_name='فعال')

    def __str__(self):
        return f'{self.user}/{self.product}/{self.active}/{self.body[:10]}'

    class Meta:
        verbose_name_plural = "نظرات  محصول"
