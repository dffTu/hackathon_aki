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
