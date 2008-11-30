Static Management
=================

This project is intended as an easy way to manage multiple static text assets (CSS and Javascript) in a Django projects.

Currently includes:
-------------------

* A template tag to echo collections of CSS files;
* A combination function with optional delimter;
* A sample Django project using the template tags.

Will (eventually) include:
-------------

* JS as well as CSS template tags;
* Support for time stamped file names (for far-future-expires);
* A Django management command to combine files (for building);
* Support for command line minification/compression when building (YUI compressor, JSMin, Icy etc.);
* Unit tests;
* Sample web server configuration for Gzip, mod\_deflate etc. (since you really shouldn't be serving static assets via Django in production).

Usage
-----

The configuration is intended to be easy to read and use.

### Settings

Add the following construct (or similar) in `settings.py`:

    STATIC_MANAGEMENT = {
        'css': {
            'css/mymainfile.css' : [
                'css/myfile',
                'css/anotherfile'
            ],
        }
    }

What happens is that files inside `css` are combined as follows:

1. `css/mymainfile.css` is the target file, which is created automatically from the list of files beside it;
2. If the files do not exist, the entire file is skipped;
3. Paths are *relative* to `settings.MEDIA_ROOT` (so you're unlikely to need to move files around in an already working Django project).

Other files may inherit from `css/mymainfile.css` (for example, IE hack fles) by including it in their list of files, like so:

    ...
    'css/myie6.css' : [
        'css/mymainfile.css', # inherits from main
        'css/ie6.css'
    ]
    ...

### Templates

In your templates, you use the `static_combo` template tag library:

    {% load static_combo %}
    {% static_combo_css "css/main.css" %}

Where `css/mymainfile.css` is the "combined" file name from your settings. In `DEBUG` mode, this will echo out all the files in order (for debugging purposes). In production mode, it will only echo the "combined" file name.

By default it uses HTML 4.01 style `link` elements (non self-closing) - you may override this with a setting like:

    STATIC_MANAGEMENT_CSS_LINK = '<link rel="stylesheet" type="text/css" href="%s" />\n'

License
-------

This work contains some samples of the [YUI](http://developer.yahoo.com/yui/) library, which is licensed under a [BSD License](http://developer.yahoo.com/yui/license.html). My own work here is licensed similarly.