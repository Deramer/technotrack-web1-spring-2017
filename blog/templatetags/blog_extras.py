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
