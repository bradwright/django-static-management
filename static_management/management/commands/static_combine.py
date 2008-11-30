import os

from django.core.management.base import BaseCommand
from django.conf import settings

from static_management.lib import static_combine as combine_files

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            css_files = settings.STATIC_MANAGEMENT['css']
        except AttributeError:
            print "Static CSS files not provided. You must provide a set of files to combine."
            raise SystemExit
        for main_file in css_files.keys():
            main_file_path = os.path.join(settings.MEDIA_ROOT, main_file)
            files = settings.STATIC_MANAGEMENT['css'][main_file]
            sub_file_paths = []
            for sub_file in files:
                file_path = os.path.join(settings.MEDIA_ROOT, sub_file)
                if os.path.exists(file_path):
                    sub_file_paths.append(file_path)
            combine_files(main_file_path, sub_file_paths)
            