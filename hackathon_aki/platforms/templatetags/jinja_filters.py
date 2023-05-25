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
