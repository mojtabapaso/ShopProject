import logging

from django.utils import timezone

from models import User

local_time = timezone.localtime(timezone.now())
logger = logging.getLogger(__name__)


def services_create_user(phone_number, password):
    try:
        User.objects.create(phone_number, password)
    except Exception as e:
        logger.warning(f"Name : {logger.name} | Time {local_time} : Error {e}")
    return None


def get_user_by_id(id):
    try:
        user = User.objects.get(id)
        return user

    except Exception as e:
        logger.error(f"Name : {logger.name} | Time {local_time}  : Error {e}")


def get_user_by_phone_number(phone_number):
    try:
        user = User.objects.get(phone_number=phone_number)
        return user

    except Exception as e:
        logger.error(f"Name : {logger.name} | Time {local_time}  : Error {e}")
