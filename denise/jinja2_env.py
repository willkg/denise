from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse

from jinja2 import Environment


def environment(*args, **kwargs):
    env = Environment(*args, **kwargs)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url_for': reverse
    })
    return env
