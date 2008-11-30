Static Management
=================

This project is intended as an easy way to manage multiple static text assets (CSS and Javascript) in a Django projects.

Currently includes:
-------------------

* A template tag to echo collections of CSS files;
* A combination function with optional delimter;
* A sample Django project using the template tags;
* JS as well as CSS template tags;
* A Django management command to combine files (for building).

Will (eventually) include:
-------------

* Support for time stamped file names (for far-future-expires);
* Support for command line minification/compression when building (YUI compressor, JSMin, Icy etc.);
* Unit tests;
* Sample web server configuration for Gzip, mod\_deflate etc. (since you really shouldn't be serving static assets via Django in production).

Usage
-----

The configuration is intended to be easy to read and use.

Add the `static_management` directory into your Django application, and included it in `installed_apps`.

### Settings

Add the following construct (or similar) in `settings.py`:

    STATIC_MANAGEMENT = {
        'css': {
            'css/mymainfile.css' : [
                'css/myfile.css',
                'css/anotherfile.css'
            ],
        }
        'js': {
            'js/myjsfile.js' : [
                'js/mynewfile.js',
                'js/anotherfile.js'
            ],
        }
    }

What happens is that files inside `css` and `js` are combined as follows:

1. `css/mymainfile.css` (the "key" of the key/value pair) is the target file, which is created automatically from the list of files (the "value" of the key/value pair) beside it;
2. If the files do not exist, the entire file is skipped;
3. Paths are *relative* to `settings.MEDIA_ROOT` (so you're unlikely to need to move files around in an already working Django project).

Other files may inherit from `css/mymainfile.css` (for example, IE hack files) by including it in their list of files, like so:

    ...
    'css/myie6.css' : [
        'css/mymainfile.css', # inherits from main
        'css/ie6.css'
    ]
    ...

### Templates

In your templates, you use the `static_combo` template tag library:

    {% load static_combo %}
    {% static_combo_css "css/mymainfile.css" %}
    ... rest of page ...
    {% static_combo_js "js/myjsfile.js" %}

Where `css/mymainfile.css` is the "combined" file name from your settings. In `DEBUG` mode, this will echo out all the files in order (for debugging purposes). In production mode, it will only echo the "combined" file name.

By default the CSS template tag uses HTML 4.01 style `link` elements (non self-closing) - you may override this with a setting like:

    STATIC_MANAGEMENT_CSS_LINK = '<link rel="stylesheet" type="text/css" href="%s" />\n'

The Javascript template tag uses the standard construct, and only needs to be overridden if you want to force UTF-8 encoding in your files:

    STATIC_MANAGEMENT_JS_LINK = '<script type="text/javascript" charset="utf-8" src="%s"></script>\n'

License
-------

This work contains some samples of the [YUI](http://developer.yahoo.com/yui/) library, which is licensed under a [BSD License](http://developer.yahoo.com/yui/license.html). My own work here is licensed similarly.