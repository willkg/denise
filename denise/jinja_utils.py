from __future__ import unicode_literals, print_function
import functools
import imp

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
from django.http import QueryDict
from django.template.defaulttags import CsrfTokenNode
from django.utils import six
from django.utils.encoding import smart_str
try:
    from django.utils.encoding import smart_unicode as smart_text
except ImportError:
    from django.utils.encoding import smart_text
from django.utils.http import urlencode
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

import jinja2


class Register(object):
    """Decorators to add filters and functions to the template Environment."""

    def __init__(self):
        self.globals = {}
        self.filters = {}

    def filter(self, f=None, override=True):
        """Adds the decorated function to Jinja's filter library."""
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kw):
                return f(*args, **kw)
            return self.filter(wrapper, override)

        if not f:
            return decorator
        if override or f.__name__ not in self.filters:
            self.filters[f.__name__] = f
        return f

    def function(self, f=None, override=True):
        """Adds the decorated function to Jinja's global namespace."""
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kw):
                return f(*args, **kw)
            return self.function(wrapper, override)

        if not f:
            return decorator
        if override or f.__name__ not in self.globals:
            self.globals[f.__name__] = f
        return f

    # FIXME: This needs an environment to work, but we don't have one
    # to use.
    # def inclusion_tag(self, template):
    #     """Adds a function to Jinja, but like Django's @inclusion_tag."""
    #     def decorator(f):
    #         @functools.wraps(f)
    #         def wrapper(*args, **kw):
    #             context = f(*args, **kw)
    #             t = BASE_ENV.get_template(template).render(context)
    #             return jinja2.Markup(t)
    #         return self.function(wrapper)
    #     return decorator


register = Register()

# Indicates whether we've loaded the helpers already or not. We onlt
# want to do it once.
_helpers_loaded = False


def load_helpers(force_reload=False):
    """Try to import ``helpers.py`` from each app in INSTALLED_APPS.

    :arg force_reload: If True, will go through and reload all the
        helpers

    """
    global _helpers_loaded
    if _helpers_loaded and not force_reload:
        return
    _helpers_loaded = True

    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('helpers', app_path)
        except ImportError:
            continue

        import_module('%s.helpers' % app)


def environment(*args, **kwargs):
    """Builds a new Jinja2 environment and returns it"""
    load_helpers()
    env = jinja2.Environment(*args, **kwargs)
    env.globals.update(register.globals)
    env.filters.update(register.filters)
    return env


@register.function
@jinja2.contextfunction
def csrf(context):
    return jinja2.Markup(CsrfTokenNode().render(context))


@register.function
def static(path):
    return staticfiles_storage.url(path)


@register.filter
def f(string, *args, **kwargs):
    """
    Uses ``str.format`` for string interpolation.

    >>> {{ "{0} arguments and {x} arguments"|f('positional', x='keyword') }}
    "positional arguments and keyword arguments"
    """
    return string.format(*args, **kwargs)


@register.filter
def fe(string, *args, **kwargs):
    """
    Format safe string with possibly unsafe arguments and return safe string
    """
    string = six.text_type(string)

    args = [jinja2.escape(smart_text(v)) for v in args]

    for k in kwargs:
        kwargs[k] = jinja2.escape(smart_text(kwargs[k]))

    return jinja2.Markup(string.format(*args, **kwargs))


@register.filter
def nl2br(text):
    """Turn newlines into ``<br>``"""
    if not text:
        return ''
    return jinja2.Markup('<br>'.join(jinja2.escape(text).splitlines()))


@register.filter
def datetime(t, fmt=None):
    """Call ``datetime.strftime`` with the given format string"""
    if fmt is None:
        fmt = _(u'%B %e, %Y')
    if not six.PY3:
        # The datetime.strftime function strictly does not
        # support Unicode in Python 2 but is Unicode only in 3.x.
        fmt = fmt.encode('utf-8')
    return smart_text(t.strftime(fmt)) if t else ''


@register.filter
def ifeq(a, b, text):
    """Return ``text`` if ``a == b``"""
    return jinja2.Markup(text if a == b else '')


@register.filter
def class_selected(a, b):
    """Return ``'class="selected"'`` if ``a == b``."""
    return ifeq(a, b, 'class="selected"')


@register.filter
def field_attrs(field_inst, **kwargs):
    """Adds html attributes to django form fields"""
    for k, v in kwargs.items():
        if v is not None:
            field_inst.field.widget.attrs[k] = v
        else:
            field_inst.field.widget.attrs.pop(k, None)
    return field_inst


@register.function(override=False)
def url(viewname, *args, **kwargs):
    """Return URL using django's ``reverse()`` function"""
    return reverse(viewname, args=args, kwargs=kwargs)


@register.filter
def urlparams(url_, fragment=None, query_dict=None, **query):
    """
    Add a fragment and/or query parameters to a URL.

    New query params will be appended to exising parameters, except duplicate
    names, which will be replaced.
    """
    url_ = urlparse.urlparse(url_)
    fragment = fragment if fragment is not None else url_.fragment

    q = url_.query
    new_query_dict = (QueryDict(smart_str(q), mutable=True) if
                      q else QueryDict('', mutable=True))
    if query_dict:
        for k, l in query_dict.lists():
            new_query_dict[k] = None  # Replace, don't append.
            for v in l:
                new_query_dict.appendlist(k, v)

    for k, v in query.items():
        # Replace, don't append.
        if isinstance(v, list):
            new_query_dict.setlist(k, v)
        else:
            new_query_dict[k] = v

    query_string = urlencode([(k, v) for k, l in new_query_dict.lists() for
                              v in l if v is not None])
    new = urlparse.ParseResult(url_.scheme, url_.netloc, url_.path,
                               url_.params, query_string, fragment)
    return new.geturl()
