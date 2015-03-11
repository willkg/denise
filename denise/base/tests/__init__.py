import unittest

from django.test import Client


def eq_(a, b, msg=None):
    if msg is None:
        msg = '{0} != {1}'.format(repr(a), repr(b))
    assert a == b, msg


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
