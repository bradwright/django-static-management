import os
import sys

from django.conf import settings

try:
    import yaml
except ImportError:
    pass

__all__ = ['YamlWriter']

class YamlWriter(object):
    """Writes the version map to a YAML file"""
    def __call__(self, versions):
        obj = {'STATIC_MANAGEMENT_VERSIONS': versions}
        # Clobber existing YAML file
        fstream = open(settings.STATIC_MANAGEMENT_YAML_FILE, mode='w')
        try:
            yaml.dump(obj, stream=fstream)
        finally:
            fstream.close()
