import os
from optparse import OptionParser, make_option

from django.core.management.base import BaseCommand
from django.conf import settings

from static_management.lib import static_combine

class Command(BaseCommand):
    """static management commands for static_combine argument"""
    
    option_list = BaseCommand.option_list + (
        make_option("-c", "--compress", action="store_true", dest="compress", default=False, help='Runs the compression script defined in "STATIC_MANAGEMENT_COMPRESS_CMD" on the final combined files'),
    )
    
    def handle(self, *args, **kwargs):
        self.options = kwargs
        self.files_created = []
        self.combine_js()
        self.combine_css()
    
    def combine_js(self):
        try:
            js_files = settings.STATIC_MANAGEMENT['js']
        except AttributeError:
            print "Static JS files not provided. You must provide a set of files to combine."
            raise SystemExit
        combine_files(js_files, self.options)
    
    def combine_css(self):
        try:
            css_files = settings.STATIC_MANAGEMENT['css']
        except AttributeError:
            print "Static CSS files not provided. You must provide a set of files to combine."
            raise SystemExit
        combine_files(css_files, self.options)
    
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
