import os

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
            if css_file in settings.STATIC_MANAGEMENT['css'].keys():
                # we need to get all the 'inherited' files
                output += static_combo_css(css_file)
            else:
                if os.path.exists(file_path):
                    output += link_format % os.path.join(settings.MEDIA_URL, css_file)
                else:
                    # error out, we can't combine files
                    raise template.TemplateSyntaxError, "%s does not exist" % file_path
    else:
        # return "combined" files
        output = link_format % "%s%s" % (settings.MEDIA_URL, filename)
    return output

@register.simple_tag
def static_combo_js(filename):
    """combines files in settings
    
    {% static_combo_js "js/main.js" %}"""
    try:
        # Splitting by None == splitting by spaces.
        files = settings.STATIC_MANAGEMENT.get('js').get(filename)
    except AttributeError:
        raise template.TemplateSyntaxError, "%s not in static combo settings" % filename
    # override the default if an override exists
    try:
        script_format = settings.STATIC_MANAGEMENT_SCRIPT_SRC
    except AttributeError:
        script_format = '<script type="text/javascript" src="%s"></script>\n'
    output = ''
    if settings.DEBUG:
        # we need to echo out each one
        for js_file in files:
            file_path = os.path.join(settings.MEDIA_ROOT, js_file)
            media_url = settings.MEDIA_URL
            if js_file in settings.STATIC_MANAGEMENT['js'].keys():
                # we need to get all the 'inherited' files
                output += static_combo_css(js_file)
            else:
                if os.path.exists(file_path):
                    output += script_format % os.path.join(settings.MEDIA_URL, js_file)
                else:
                    # error out, we can't combine files
                    raise template.TemplateSyntaxError, "%s does not exist" % file_path
    else:
        # return "combined" files
        output = script_format % "%s%s" % (settings.MEDIA_URL, filename)
    return output
