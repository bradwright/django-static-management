import os
import sys

from django import template
from django.conf import settings
from static_management.lib import static_combine

register = template.Library()

@register.simple_tag
def static_combo_css(filename):
    """combines files in settings
    
    {% static_combo_css "css/main.css" %}"""
    try:
        # Splitting by None == splitting by spaces.
        files = settings.STATIC_MANAGEMENT.get('css').get(filename)
    except AttributeError:
        raise template.TemplateSyntaxError, "%s not in static combo settings" % filename
    # override the default if an override exists
    try:
        link_format = settings.STATIC_MANAGEMENT_CSS_LINK
    except AttributeError:
        link_format = '<link rel="stylesheet" type="text/css" href="%s">\n'
    output = ''
    if settings.DEBUG:
        # we need to echo out each one
        for css_file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, css_file)
            media_url = settings.MEDIA_URL
            if os.path.exists(file_path):
                output += link_format % os.path.join(settings.MEDIA_URL, css_file)
            else:
                # error out, we can't combine files
                raise template.TemplateSyntaxError, "%s does not exist" % file_path
    else:
        # return "combined" files
        output = link_format % "%s%s" % (settings.MEDIA_URL, filename)
    return output

"""    # NOTE: This should never happen, as we provide a management script to
    # do this for you, and you should be serving your files via something 
    # other than Django
    file_paths = []
    for css in files:
        file_paths.append(os.path.join(settings.MEDIA_ROOT, css))
    combo_file_path = os.path.join(settings.MEDIA_ROOT, filename)
    static_combine(combo_file_path, file_paths)"""