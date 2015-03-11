from unittest import TestCase

from denise.base.utils import translate_site, translate_text
from denise.base.tests import eq_


class TranslateTextTestCase(TestCase):
    def test_basic(self):
        eq_(translate_text(u'abcd'), 'abZZGB CZCPT!')


class TranslateSiteTestCase(TestCase):
    def test_basic(self):
        html = u'<html><body><h1>Best site ever!</h1></body></html>'
        eq_(translate_site('http://example.com/', html),
            u'<html><body><h1>BHARZHG RZARHGHA HABBHAMZ\u2757</h1></body></html>'
        )

    # FIXME: test link fixing
