import os

from django.core.management.base import BaseCommand
from django.conf import settings

from static_management.lib import static_combine as combine_files

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.files_created = []
        self.combine_js()
        self.combine_css()
    
    def combine_js(self):
        try:
            js_files = settings.STATIC_MANAGEMENT['js']
        except AttributeError:
            print "Static JS files not provided. You must provide a set of files to combine."
            raise SystemExit
        self._combine_files(js_files, 'js')
    
    def combine_css(self):
        try:
            css_files = settings.STATIC_MANAGEMENT['css']
        except AttributeError:
            print "Static CSS files not provided. You must provide a set of files to combine."
            raise SystemExit
        self._combine_files(css_files, 'css')
    
    def _combine_files(self, files, inheritance_key):
        parent_files = files.keys()
        for main_file in parent_files:
            main_file_path = os.path.join(settings.MEDIA_ROOT, main_file)
            files = settings.STATIC_MANAGEMENT[inheritance_key][main_file]
            sub_file_paths = []
            for sub_file in files:
                file_path = os.path.join(settings.MEDIA_ROOT, sub_file)
                if sub_file in parent_files:
                    if sub_file in self.files_created:
                        # file has been made - copy
                        pass
                    else:
                        pass
                if os.path.exists(file_path):
                    sub_file_paths.append(file_path)
            combine_files(main_file_path, sub_file_paths)
            self.files_created.append(main_file)
    
