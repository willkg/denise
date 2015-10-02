from unittest import TestCase

from denise.base.utils import translate_site, translate_text
from denise.base.tests import eq_


class TranslateTextTestCase(TestCase):
    def test_zombie(self):
        eq_(translate_text('zombie', u'oh my goddness!'),
            u'HRh mRA gHRGBGBnHARZRZ\u2757'
        )

    def test_dubstep(self):
        eq_(translate_text('dubstep', u'oh my goodness!'),
            u'oh my t-t-t-t goodness! BWWWWWAAAAAAAaaaaa\u2757'
        )

    def test_pirate(self):
        eq_(translate_text('pirate', u'oh my goodness!'),
            u'oh me goodness arrRRRrrr\u2757\u2757'
        )


class TranslateSiteTestCase(TestCase):
    def test_zombie(self):
        html = u'<html><body><h1>Best site ever!</h1></body></html>'
        eq_(translate_site('zombie', 'http://example.com/', html),
            u'<html><body><h1>BHARZHG RZARHGHA HABBHAMZ\u2757</h1></body></html>'
        )

    def test_dubstep(self):
        html = u'<html><body><h1>Best site ever!</h1></body></html>'
        eq_(translate_site('dubstep', 'http://example.com/', html),
            u'<html><body><h1>Best site ....vvvVV ever! BWWWWWWAAAAAAAAaaaaaa\u2757</h1></body></html>'
        )

    def test_pirate(self):
        html = u'<html><body><h1>Best site ever!</h1></body></html>'
        eq_(translate_site('pirate', 'http://example.com/', html),
            u'<html><body><h1>Best site everr matey\u2757\u2757</h1></body></html>'
        )

    # FIXME: test link fixing
