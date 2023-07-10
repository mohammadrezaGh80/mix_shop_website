from django import template

import html

register = template.Library()


@register.filter
def replace_dash_with_space_category_name(category_name):
    category_name = html.unescape(category_name)
    return category_name.replace("-", " ")


@register.filter
def is_user_liked_comment(comment, user):
    return comment.likes.filter(user=user).exists()


@register.filter
def is_user_disliked_comment(comment, user):
    return comment.dislikes.filter(user=user).exists()


@register.filter
def is_user_liked_answer(answer, user):
    return answer.likes.filter(user=user).exists()


@register.filter
def is_user_disliked_answer(answer, user):
    return answer.dislikes.filter(user=user).exists()
