import json
import sys

from distutils.errors import DistutilsSetupError
from setuptools import Command

__version__ = '1.0.0'
__description__ = 'Easily store custom metadata with setuptools'


def setup_keyword(dist, attr, value):
    if not isinstance(value, dict):
        raise DistutilsSetupError("'meta' should be a dict")


def egg_info(cmd, basename, filename):
    '''An egg_info.writers that store custom metadata into json'''
    cmd.write_or_delete_file('meta', filename, json.dumps(cmd.distribution.meta))


class MetaCommand(Command):
    description = 'Store extra metadata to meta.json (before egg_info)'

    user_options = [
        ('key=', 'k', 'meta key to add'),
        ('value=', None, 'meta value to add'),  # -v is already used by verbose
    ]

    def initialize_options(self):
        self.key = None
        self.value = None

    def finalize_options(self):
        if self.key is None:
            raise DistutilsSetupError('Option --key is required')

        if self.value is None:
            raise DistutilsSetupError('Option --value is required')

    def run(self):
        self.distribution.meta[self.key] = self.value
