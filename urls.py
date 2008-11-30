from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.home'),
    # Example:
    # (r'^static_mgmt/', include('static_mgmt.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)

# this is for serving static files in development
if settings.DEBUG:
    import os
    # get the static path from settings
    static_url = settings.MEDIA_URL
    if static_url.startswith('/'):
        static_url = static_url.lstrip('/')
    urlpatterns += patterns('',
        (
            r'^%s(?P<path>.*)$' % static_url,
            'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT
            }
        ),
    )
