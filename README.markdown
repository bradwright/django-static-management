Static Management
=================

This project is intended as an easy way to manage multiple static text assets (CSS and Javascript) in a Django projects.

Currently includes:
-------------------

* A template tag to echo collections of CSS files;
* A combination function with optional delimter;
* A sample Django project using the template tags;
* JS as well as CSS template tags;
* A Django management command to combine files (for building);
* Support for command line minification/compression when building (YUI compressor, JSMin, Icy etc.).
* Support for filename versioning (using SHA1 sums, file modification times, etc.).

Will (eventually) include:
-------------

* Unit tests;
* Sample web server configuration for Gzip, mod\_deflate etc. (since you really shouldn't be serving static assets via Django in production).

Usage
-----

The configuration is intended to be easy to read and use.

Add the `static_management` directory into your Django application, and included it in `installed_apps`.

You can include the current version as a `git submodule` as follows:

    git submodule add git://github.com/bradleywright/django-static-management.git django_site_dir/static_management

Substitute `django_site_dir` with the root directory of your Django application (where `manage.py` and `settings.py` live).

### Settings

Add the following construct (or similar) in `settings.py`:

    STATIC_MANAGEMENT = {
        'css': {
            'css/mymainfile.css' : [
                'css/myfile.css',
                'css/anotherfile.css'
            ],
        },
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

    STATIC_MANAGEMENT_SCRIPT_SRC = '<script type="text/javascript" charset="utf-8" src="%s"></script>\n'

### File versioning

In order to help meet [performance recommendations](http://developer.yahoo.net/blog/archives/2007/05/high_performanc_2.html) which encourage the use of `Expires:` headers, static management supports versioning files.

To use, simply define a dictionary that maps relative filenames to versioned filenames:

    STATIC_MANAGEMENT_VERSIONS = {
        'js/main.js': 'js/main.12345.js'
    }

#### Version class

Specify the type of file versioning with a setting like:

    STATIC_MANAGEMENT_VERSIONER = 'static_management.versioners.SHA1Sum'

The following pre-rolled versioners are included:

* `SHA1Sum` - Calculates the SHA1 sum of a file's contents and uses the first 8 characters for the version
* `MD5Sum` - Same as `SHA1Sum` but using the MD5 algorithm instead
* `FileTimestamp` - Uses the UNIX time representation of the file modification time to generate a version

Custom versioners are simple callables that take a single filename argument.

### Management commands

The following command will generate all the files as per your settings:

    ./manage.py static_combine

#### Compression

Passing an argument of `--compress` to the above command will run the compression script of your choice, as specified in: `settings.STATIC_MANAGEMENT_COMPRESS_CMD`. This should be a string representing the script you want to run. The only caveat is that it must accept a filepath as an argument and return output to `stdout` (the management command reads from `stdout`). Following is an example using YUI Compressor (which this command was designed to use):

    # settings.py
    STATIC_MANAGEMENT_COMPRESS_CMD = 'java -jar /home/myuser/yuicompressor-2.4.2/build/yuicompressor-2.4.2.jar %s'

where `%s` represents the path of the file to be compressed.

#### Versioning

The `--output` argument will generate a list of versioned filenames and output them using the method of your choice, as specified in: `settings.STATIC_MANAGEMENT_VERSION_WRITER`.  This should be a callable which takes a dictionary of the structured defined above in `STATIC_MANAGEMENT_VERSIONS`.

Note: It is often useful to use this mechanism to write the list of files to a configuration file and read from the same file in `settings.py`.

The `--version` argument will copy the relatively filename (e.g. `js/main.js`) to the versioned filename (e.g. `js/main.123456.js`).

Using this within a Django project
----------------------------------

The [1.0 tag](http://github.com/bradleywright/django-static-management/tree/1.0) of this project contains a sample Django project to help demonstrate usage. This code structure will not be followed beyond the initial version--a `git submodule` is now the preferred way of using this application.

License
-------

This work contains some samples of the [YUI](http://developer.yahoo.com/yui/) library, which is licensed under a [BSD License](http://developer.yahoo.com/yui/license.html). My own work here is licensed similarly.
