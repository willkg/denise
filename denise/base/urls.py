from django.conf import settings
from django.conf.urls import url
import django.views.static

import denise.base.views


urlpatterns = [
    url(r'^$', denise.base.views.index_view, name='index-view'),
    url(r'^lint/', denise.base.views.lint_view, name='lint-view'),

    url(r'^(?P<path>favicon\.ico)$', django.views.static.serve,
        {'document_root': settings.BASE_DIR + '/denise/base/static'}),
]
