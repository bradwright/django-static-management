import os

from django import template
from django.conf import settings
from static_management.lib import static_combine

register = template.Library()

@register.simple_tag
def static_asset(file_name):
    """produces the full versioned path for a static asset

    <img alt="Logo" src="{% static_asset "img/logo.png" %}>"""
    try:
        return settings.STATIC_MANAGEMENT_VERSIONS[file_name]
    except AttributeError:
        raise template.TemplateSyntaxError, "%s not in static version settings" % file_name
