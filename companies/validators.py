import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def phone_num_validator(number: str):
    '''
    Validates given phone number format.
    Valid formats are: +18005553535 or 88005553535
    Min phone length is 8, max is 12
    '''
    num_re = re.compile(r'\+?[0-9]{8,12}')
    if not num_re.match(number):
        raise ValidationError(
            _(f'{number} has wrong phone number format')
        )