import logging

from django.shortcuts import get_object_or_404
from django.utils import timezone
from products.models import Brand, Products, Commend

from .models import Category

local_time = timezone.localtime(timezone.now())
logger = logging.getLogger(__name__)


def services_create_user(phone_number, password):
    try:
        User.objects.create(phone_number, password)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_main_categories():
    try:
        return Category.objects.filter(is_sub_category=False)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_active_products():
    try:
        return Products.objects.filter(is_active=True)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_all_brands():
    try:
        return Brand.objects.all()
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_product_by_slug(slug):
    try:
        return get_object_or_404(Products, slug=slug)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_product_by_id(id):
    try:
        return get_object_or_404(Products, id=id)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_commend_by_id(commend_id):
    try:
        return get_object_or_404(Commend, pk=commend_id)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_active_commends():
    try:
        return Commend.objects.filter(active=True, is_reply=False)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def get_brand_by_slug(slug):
    try:
        return Brand.objects.get(slug=slug)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def filter_products_by_brand(brand_slug):
    try:
        brand = get_brand_by_slug(brand_slug)
        return Products.filter(is_active=True, brand=brand)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def filter_products_by_category(slug_category):
    try:
        category = Category.objects.filter(slug=slug_category)
        product = Products.filter(category__in=category)
        return product
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def search_products(products, search_query):
    try:
        return products.filter(title__contains=search_query)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def filter_category_by_slug(slug):
    try:
        category = Category.objects.filter(slug)
        return category
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def filter_product_by_title(search_query):
    try:
        products = Products.filter(title__contains=search_query)
        return products
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def filter_by_price_range(filter_min, filter_max):
    try:
        if filter_min and filter_max:
            products = Products.filter(price__range=(filter_min, filter_max))
            return products
        return None
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")


def filter_by_price_range_and_max(filter_min):
    try:
        products = get_active_products()

        filter = [item.price for item in products]
        max_price = max(filter)

        if filter_min:
            products = products.filter(price__range=(filter_min, max_price))

        return products
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")
