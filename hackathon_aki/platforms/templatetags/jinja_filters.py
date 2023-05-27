import datetime
from django import template

register = template.Library()


@register.filter(name="key")
def get_key(value, arg):
    return value[arg]


@register.filter(name="join")
def join(value, arg):
    return arg.join(value)


@register.filter(name="split")
def split(value, arg):
    return value.split(arg)


@register.filter(name='shorten_text')
def shorten_text(value, arg):
    if len(value) <= arg:
        return value
    return value[:max(0, arg - 3)] + '...'


@register.filter(name='get_date')
def shorten_text(value):
    return value.date()


@register.filter(name='get_date')
def shorten_text(value):
    return value.date()


@register.filter(name='get_all')
def shorten_text(value):
    return value.all()


@register.filter(name='round')
def shorten_text(value, arg):
    return round(value, arg)


@register.filter(name='range')
def shorten_text(value, arg):
    return range(value, arg)
