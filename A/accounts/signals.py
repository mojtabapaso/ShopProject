from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, OtpCode
import datetime


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    # for create model profile user
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


@receiver(post_save, sender=OtpCode)
def update_otp_code(sender, **kwargs):
    # for create expire time code minutes=2
    if kwargs['created']:
        OtpCode.objects.update(expire=kwargs['instance'].create + datetime.timedelta(minutes=2))
