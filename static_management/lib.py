import os
import sys
import subprocess

from django.conf import settings
from django.core.management.base import CommandError

def static_combine(end_file, to_combine, delimiter="\n/* Begin: %s */\n", compress=False):
    """joins paths together to create a single file
    
    Usage: static_combine(my_ultimate_file, list_of_paths, [delimiter])
    
    delimiter is set to a Javascript and CSS safe comment to note where files 
    start"""
    # open and clobber file
    combo_file = open(end_file, 'w')
    to_write = ''
    for static_file in to_combine:
        if os.path.isfile(static_file):
            if delimiter:
                to_write += delimiter % os.path.split(static_file)[1]
            to_write += file(static_file).read()
    if to_write:
        combo_file.write(to_write)
        combo_file.close()
        if compress:
            try:
                command =  settings.STATIC_MANAGEMENT_COMPRESS_CMD % end_file
            except AttributeError, error:
                raise CommandError("STATIC_MANAGEMENT_COMPRESS_CMD not set")
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            to_write = proc.communicate()[0]
            compressed_file = open(end_file, 'w')
            compressed_file.write(to_write)
            compressed_file.close()