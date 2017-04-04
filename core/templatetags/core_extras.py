from django import template

from blog.models import Post


register = template.Library()


@register.simple_tag(takes_context=True)
def produce_get(context, **kwargs):
    get = context['request'].GET.copy()
    for key, value in kwargs.items():
        get[key] = value
    return '?' + get.urlencode()


@register.simple_tag(takes_context=True)
def produce_get_update(context, **kwargs):
    get = context['request'].GET.copy()
    for key, value in kwargs.items():
        get.appendlist(key, value)
    return '?' + get.urlencode()


@register.simple_tag(takes_context=True)
def produce_get_remove(context, **kwargs):
    get = context['request'].GET.copy()
    for key, value in kwargs.items():
        key_list = get.getlist(key)
        key_list.remove(value)
        get.setlist(key, key_list)
    return '?' + get.urlencode()


@register.filter
def querydict_get_list(querydict, key):
    return querydict.getlist(key)


@register.inclusion_tag('core/sidebar.html')
def fill_sidebar():
    return {'list': Post.objects.order_by('-created_at')[:9]}
