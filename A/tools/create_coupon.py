import string
import random



def create_coupon():
    """ create coupon
    use : number 1 to 9 and letters english upper and small
    output : code random 11 digit
    """
    value = string.ascii_letters + '123456789'
    coupon = ''
    for i in range(11):
        coupon += "".join(random.choice(value))
    return coupon