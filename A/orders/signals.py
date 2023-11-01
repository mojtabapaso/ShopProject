from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Coupon, Cart, Order
from .create_coupon import create_coupon


@receiver(post_save, sender=Coupon)
def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        code = Coupon.objects.filter(user=instance.user)
        for i in code:
            i.code = create_coupon()
            i.save()
