from django import template

register = template.Library()


@register.filter(name="key")
def get_key(value, arg):
    return value[arg]


@register.filter(name="join")
def join_with_divider(value, arg):
    return arg.join(value)
