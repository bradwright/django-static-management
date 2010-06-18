import os
import time

from django import template
from django.conf import settings
from static_management.lib import static_combine

register = template.Library()

@register.simple_tag
def static_combo_css(file_name, media=None):
    """combines files in settings
    
    {% static_combo_css "css/main.css" %}"""
    # override the default if an override exists
    try:
        link_format = settings.STATIC_MANAGEMENT_CSS_LINK
    except AttributeError:
        if media:
            link_format = '<link rel="stylesheet" type="text/css" href="%%s" media="%s">\n' % media
        else:
            link_format = '<link rel="stylesheet" type="text/css" href="%s">\n'
    output = _group_file_names_and_output(file_name, link_format, 'css')
    return output

@register.simple_tag
def static_combo_js(file_name):
    """combines files in settings
    
    {% static_combo_js "js/main.js" %}"""
    # override the default if an override exists
    try:
        script_format = settings.STATIC_MANAGEMENT_SCRIPT_SRC
    except AttributeError:
        script_format = '<script type="text/javascript" src="%s"></script>\n'
    output = _group_file_names_and_output(file_name, script_format, 'js')
    return output

def _group_file_names_and_output(parent_name, output_format, inheritance_key):
    """helper function to do most of the heavy lifting of the above template tags"""
    try:
        file_names = settings.STATIC_MANAGEMENT[inheritance_key][parent_name]
    except AttributeError:
        raise template.TemplateSyntaxError, "%s not in static combo settings" % parent_name
    output = ''
    if settings.DEBUG:
        # we need to echo out each one
        media_url = settings.MEDIA_URL
        for file_name in file_names:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if file_name in settings.STATIC_MANAGEMENT[inheritance_key]:
                output += _group_file_names_and_output(file_name, output_format, inheritance_key)
            else:
                if os.path.exists(file_path):
                    # need to append a cachebust as per static_asset
                    to_output = output_format % os.path.join(settings.MEDIA_URL, file_name)
                    if hasattr(settings, 'STATIC_MANAGEMENT_CACHEBUST') and settings.STATIC_MANAGEMENT_CACHEBUST:
                        to_output += "?cachebust=%s" % time.time()
                    output += to_output
                else:
                    raise template.TemplateSyntaxError, "%s does not exist" % file_path
    else:
        try:
            parent_name = settings.STATIC_MANAGEMENT_VERSIONS[parent_name]
        except (AttributeError, KeyError):
            raise template.TemplateSyntaxError, "%s not in static version settings" % parent_name
        # return "combined" files
        output = output_format % "%s" % parent_name
    return output
