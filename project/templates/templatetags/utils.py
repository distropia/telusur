from django import template
from django.utils.html import strip_tags

register = template.Library()

@register.tag(name="html_to_text")
def html_to_text(html):
    return strip_tags(html)