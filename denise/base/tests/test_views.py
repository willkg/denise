from denise.base.tests import BaseTestCase, eq_


class FaviconTestCase(BaseTestCase):
    def test_favicon(self):
        resp = self.client.get('/favicon.ico')
        eq_(resp.status_code, 200)


class IndexViewTestCase(BaseTestCase):
    def test_index(self):
        resp = self.client.get('/')
        eq_(resp.status_code, 200)


class TextTranslateAPITestCase(BaseTestCase):
    # FIXME
    pass


class URLTranslateViewTestCase(BaseTestCase):
    # FIXME
    pass

class LintViewTestCase(BaseTestCase):
    # FIXME
    pass
