import os
import shutil
import re
from optparse import OptionParser, make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from static_management.lib import static_combine, get_version, write_versions

try:
    CSS_ASSET_PATTERN = re.compile(settings.STATIC_MANAGEMENT_CSS_ASSET_PATTERN)
except AttributeError:
    CSS_ASSET_PATTERN = re.compile('(?P<url>url(\([\'"]?(?P<filename>[^)]+\.[a-z]{3,4})(?P<fragment>#\w+)?[\'"]?\)))')

try:
    from os.path import relpath
except ImportError:
    def relpath(path, start):
        """This only works on POSIX systems and is ripped out of Python 2.6 posixpath.py"""
        start_list = os.path.abspath(start).split('/')
        path_list = os.path.abspath(path).split('/')

        # Work out how much of the filepath is shared by start and path.
        i = len(os.path.commonprefix([start_list, path_list]))

        rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return '.'
        return os.path.join(*rel_list)

class Command(BaseCommand):
    """static management commands for static_combine argument"""
    
    option_list = BaseCommand.option_list + (
        make_option("-c", "--compress", action="store_true", dest="compress", default=False, help='Runs the compression script defined in "STATIC_MANAGEMENT_COMPRESS_CMD" on the final combined files'),
        make_option("-o", "--output", action="store_true", dest="output", default=False, help='Outputs the list of filenames with version info using the "STATIC_MANAGEMENT_VERSION_OUTPUT"'),
        make_option("-w", "--write-version", action="store_true", dest="write-version", default=False, help='Produces versioned combined files in addition to non-versioned ones'),
    )
    
    def handle(self, *args, **kwargs):
        self.options = kwargs
        self.files_created = []
        self.versions = {}
        self.abs_versions = {}
        self.css_files = []
        map(self.files_created.append, self.find_assets())
        self.combine_js()
        # Do the get_versions for everything except the CSS
        self.get_versions()
        self.combine_css()
        map(self.replace_css, self.css_files)
        # Do the CSS get_versions only after having replaced all references in the CSS.
        self.get_versions(css_only=True)
        self.write_versions()
    
    def combine_js(self):
        try:
            js_files = settings.STATIC_MANAGEMENT['js']
        except AttributeError:
            print "Static JS files not provided. You must provide a set of files to combine."
            raise SystemExit(1)
        combine_files(js_files, self.options)
        map(self.files_created.append, js_files)
    
    def combine_css(self):
        try:
            css_files = settings.STATIC_MANAGEMENT['css']
        except AttributeError:
            print "Static CSS files not provided. You must provide a set of files to combine."
            raise SystemExit(1)
        combine_files(css_files, self.options)
        for file in css_files:
            self.css_files.append(file)
            self.files_created.append(file)

    def replace_css(self, filename):
        tmp = os.tmpfile()
        rel_filename = os.path.join(settings.MEDIA_ROOT, filename)
        css = open(rel_filename, mode='r')
        for line in css:
            matches = []
            for match in re.finditer(CSS_ASSET_PATTERN, line):
                try:
                    grp = match.groupdict()
                    absolute = grp['filename'].startswith('/')
                    if absolute:
                        asset_path = os.path.join(settings.MEDIA_ROOT, '.'+grp['filename'])
                    else:
                        asset_path = os.path.join(os.path.dirname(rel_filename), grp['filename'])
                    asset = relpath(asset_path, settings.MEDIA_ROOT)
                    asset_version = 'url(%s%s)' % (self.abs_versions[asset], grp.get('fragment') or '')
                    matches.append((grp['url'], asset_version))
                except KeyError:
                    print "Failed to find %s in version map. Is it an absolute path?" % asset
                    raise SystemExit(1)
            for old, new in matches:
                line = line.replace(old, new)
            tmp.write(line)
        tmp.flush()
        tmp.seek(0)
        css.close()
        css = open(rel_filename, mode='wb')
        shutil.copyfileobj(tmp, css)

    def find_assets(self):
        if settings.STATIC_MANAGEMENT_ASSET_PATHS:
            exp = re.compile(settings.STATIC_MANAGEMENT_ASSET_PATTERN)
            for path, recurse in settings.STATIC_MANAGEMENT_ASSET_PATHS:
                if recurse:
                    for root, dirs, files in os.walk(os.path.join(settings.MEDIA_ROOT, path)):
                        for filename in files:
                            if exp.match(filename):
                                yield relpath(os.path.join(root, filename), settings.MEDIA_ROOT)
                else:
                    for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, path)):
                        full_filename = os.path.join(settings.MEDIA_ROOT, os.path.join(path, filename))
                        if not os.path.isdir(full_filename):
                            if exp.match(filename):
                                yield relpath(full_filename, settings.MEDIA_ROOT)

    def get_versions(self, css_only=False):
        hosts = settings.STATIC_MANAGEMENT_HOSTNAMES
        i = 0
        if css_only:
            files = self.css_files
        else:
            files = self.files_created
        for main_file in files:
            if i > len(hosts) - 1:
                i = 0
            version = get_version(os.path.join(settings.MEDIA_ROOT, main_file), main_file, settings.STATIC_MANAGEMENT_VERSIONER)
            self.versions[main_file] = version
            self.abs_versions[main_file] = hosts[i] + version
            i += 1

    def write_versions(self):
        for main_file in self.files_created:
            if self.options['write-version']:
                shutil.copy2(os.path.join(settings.MEDIA_ROOT, main_file),
                             os.path.join(settings.MEDIA_ROOT, self.versions[main_file]))
        if self.options['output']:
            write_versions(self.abs_versions, settings.STATIC_MANAGEMENT_VERSION_WRITER)

def combine_files(files, options):
    for main_file in files:
        # create file
        main_file_path = os.path.join(settings.MEDIA_ROOT, main_file)
        # go and get sub files
        to_combine = recurse_files(main_file, files[main_file], files)
        to_combine_paths = [os.path.join(settings.MEDIA_ROOT, f_name) for f_name in to_combine if os.path.exists(os.path.join(settings.MEDIA_ROOT, f_name))]
        static_combine(os.path.join(settings.MEDIA_ROOT, main_file), to_combine_paths, compress=options['compress'])

def recurse_files(name, files, top):
    """
    given following format:
    
    {
        "filename": ["file1", "file2", "file3"],
        "filename2": ["filename", "file4"]
    }
    
    name="filename"
    files=["file1", "file2", "file3"]
    top = Whole dictionary
    
    if a value on the left appears on the right, inherit those files
    """
    combine_files = []
    for to_cat in files:
        if to_cat in top:
            combine_files.extend(recurse_files(to_cat, top[to_cat], top))
        else:
            combine_files.append(to_cat)
    return combine_files
