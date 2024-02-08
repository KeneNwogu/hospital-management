from django import template

register = template.Library()


@register.simple_tag
def underscore_tag(obj, attribute):
    obj = dict(obj)
    return obj.get(attribute)