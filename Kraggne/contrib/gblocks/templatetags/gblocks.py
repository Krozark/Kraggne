import os

from django import template

register = template.Library()


@register.filter()
def get_file_extension(f):
    """Returns the display value of a BoundField"""
    basename, ext = os.path.splitext(str(f))
    return ext.replace('.', '').lower()

