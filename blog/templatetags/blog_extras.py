from django import template

from blog.models import Comment

register = template.Library()


@register.filter(name='abs')
def my_abs(num):
    return abs(num)


@register.filter()
def check_comment_downvoted(comment):
    if comment.likes_num <= Comment.DOWNVOTED_EDGE:
        return True
    return False


@register.filter()
def get_dict_value_or_zero(dct, key):
    try:
        return dct[key]
    except KeyError:
        return 0


@register.inclusion_tag('blog/creation_form.html', takes_context=True)
def include_creation_form(context, obj_name):
    context['obj_name'] = obj_name
    return context
