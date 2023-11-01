from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import jdatetime


def validate_year(value):
    if value < 1300:
        raise ValidationError(_('year is very small'))
    if value > jdatetime.date.today().year:
        raise ValidationError(_('this time not exist'))

