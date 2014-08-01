import os

from denise.utils import truthiness


# Whether or not we're in DEBUG mode. DEBUG mode is good for
# development and BAD BAD BAD for production.
DEBUG = truthiness(os.environ.get('DEBUG', True))

# Set the SECRET_KEY in your settings_local.py file.

# TODO: Add project settings here..

# This imports settings_local.py thus everything in that file
# overrides what's in this file.
try:
    from denise.settings_local import *
except ImportError:
    pass
