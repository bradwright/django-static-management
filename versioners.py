import os
import hashlib

__all__ = ['SHA1Sum', 'MD5Sum', 'FileTimestamp']

class SHA1Sum(object):
    def __call__(self, filename):
        f = open(filename, mode='rb')
        try:
            return hashlib.sha1(f.read()).hexdigest()[:8]
        finally:
            f.close()

class MD5Sum(object):
    def __call__(self, filename):
        f = open(filename, mode='rb')
        try:
            return hashlib.md5(f.read()).hexdigest()[:8]
        finally:
            f.close()

class FileTimestamp(object):
    def __call__(self, filename):
        return str(int(os.stat(filename).st_mtime))
