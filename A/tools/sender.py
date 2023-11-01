from kavenegar import *
def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('Code')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{code} کد تایید شما '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def send_coupon(phone_number, coupon, min_cart, amount):
    try:
        api = KavenegarAPI('Code')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{coupon}کد تخفیف شما{min_cart}تومان تخفیف برای حداقل{amount} '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


