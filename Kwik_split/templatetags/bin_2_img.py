from base64 import b64encode
from django import template

register = template.Library()


@register.filter
def bin_2_img(_bin):
    if _bin is not None:
        return _bin.decode('utf-8')
