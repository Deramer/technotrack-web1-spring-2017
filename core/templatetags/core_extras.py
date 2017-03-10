from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def produce_get(context, **kwargs):
    get = context['request'].GET.copy()
    for key, value in kwargs.items():
        get[key] = value
    return '?' + get.urlencode()
