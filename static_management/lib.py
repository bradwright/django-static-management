import os
import sys

from django.conf import settings

def static_combine(end_file, to_combine, delimiter="/* Begin: %s */"):
    """joins paths together to create a single file
    
    Usage: static_combine(my_ultimate_file, list_of_paths, [delimiter])
    
    delimiter is set to a Javascript and CSS safe comment to note where files 
    start"""
    
    # open and clobber file
    combo_file = open(end_file, 'w')
    for static_file in to_combine:
        if os.path.isfile(static_file):
            if delimiter:
                combo_file.write(delimter % os.path.split(static_file)[1])
            # TODO: if some script exists in settings, run that first
            combo_file.write(file(static_file).read())
    combo_file.close()
