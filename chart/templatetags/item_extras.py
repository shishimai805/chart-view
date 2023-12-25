from django import template

register = template.Library()


@register.simple_tag
def url_index(nums:list):
    r = len(nums)
    return r
