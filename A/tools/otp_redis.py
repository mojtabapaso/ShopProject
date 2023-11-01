import hashlib
import json

import redis

from A import settings


redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)

def set_otp_code_redis(phone_number, code):
    key = hashlib.sha256(f"Phone : {phone_number} | Code : {code}".encode()).hexdigest()
    value = {"code": code}
    json_value = json.dumps(value)
    redis_client.setex(key, 120, json_value)


def validate_otp_code_redis(phone_number, code):
    key = hashlib.sha256(f"Phone : {phone_number} | Code : {code}".encode()).hexdigest()
    if redis_client.exists(key):
        redis_client.delete(key)
        return True
    return False


