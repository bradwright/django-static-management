import os
import sys
import subprocess

from django.conf import settings
from django.core import exceptions
from django.core.management.base import CommandError

def get_version(end_file, relative_filename, versioner):
    """gets the file version based on the versioner provided"""
    try:
        dot = versioner.rindex('.')
    except ValueError:
        raise exceptions.ImproperlyConfigured, '%s isn\'t a versioner' % versioner
    v_module, v_classname = versioner[:dot], versioner[dot+1:]
    try:
        mod = __import__(v_module, {}, {}, [''])
    except ImportError, e:
        raise exceptions.ImproperlyConfigured, 'Error importing versioner %s: "%s"' % (v_module, e)
    try:
        v_class = getattr(mod, v_classname)
    except AttributeError:
        raise exceptions.ImproperlyConfigured, 'Versioner module "%s" does not define a "%s" class' % (v_module, v_classname)

    version = v_class()(end_file)
    dot = relative_filename.rindex('.')
    return relative_filename[:dot+1] + version + relative_filename[dot:]

def write_versions(versions, version_writer):
    """writes the versions specified in the dictionary provided"""
    try:
        dot = version_writer.rindex('.')
    except ValueError:
        raise exceptions.ImproperlyConfigured, '%s isn\'t a version writer' % version_writer
    v_module, v_classname = version_writer[:dot], version_writer[dot+1:]
    try:
        mod = __import__(v_module, {}, {}, [''])
    except ImportError, e:
        raise exceptions.ImproperlyConfigured, 'Error importing version writer %s: "%s"' % (v_module, e)
    try:
        v_class = getattr(mod, v_classname)
    except AttributeError:
        raise exceptions.ImproperlyConfigured, 'Version writer module "%s" does not define a "%s" class' % (v_module, v_classname)
    try:
        v_class(versions)
    except TypeError:
        v_class()(versions)

def static_combine(end_file, to_combine, delimiter="\n/* Begin: %s */\n", compress=False):
    """joins paths together to create a single file
    
    Usage: static_combine(my_ultimate_file, list_of_paths, [delimiter])
    
    delimiter is set to a Javascript and CSS safe comment to note where files 
    start"""
    # FIXME this fails in the face of @import directives in the CSS.
    # a) we need to move all remote @imports up to the top
    # b) we need to recursively expand all local @imports
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
            except TypeError, error:
                raise CommandError("No string substitution provided for the input file to be passed to the argument ('cmd %s')")
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            to_write = proc.communicate()[0]
            if proc.returncode != 0:
                raise CommandError("STATIC_MANAGEMENT_COMPRESS_CMD failed to run: %s" % command)
            compressed_file = open(end_file, 'w')
            compressed_file.write(to_write)
            compressed_file.close()
