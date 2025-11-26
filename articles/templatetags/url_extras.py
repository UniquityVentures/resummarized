from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
@stringfilter
def base_url(value):
    return "https://" + value.split("/")[2]



@register.filter
@stringfilter
def favicon(value):
    return base_url(value) + "/favicon.ico"

