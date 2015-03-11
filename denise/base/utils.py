import HTMLParser
import urlparse

from dennis.translator import Translator


class LinkFixer(HTMLParser.HTMLParser):
    def __init__(self, baseurl):
        HTMLParser.HTMLParser.__init__(self)
        self.baseurl = baseurl
        self.output = []

    def fix_url(self, url):
        if not url.startswith(('http://', 'https://')):
            parts = urlparse.urlparse(self.baseurl)
            if url.startswith('//'):
                return url

            if url.startswith('/'):
                return '{0}://{1}{2}'.format(
                    parts.scheme,
                    parts.netloc,
                    url)

            path = parts.path
            if path and not path.endswith('/'):
                path = path[:path.rfind('/')]

            return '{0}://{1}/{2}{3}'.format(parts.scheme, parts.netloc, path, url)

        return url

    def handle_starttag(self, tag, attrs, closed=False):
        s = '<' + tag
        for name, val in attrs:
            s += ' '
            s += name
            s += '="'

            if val:
                if name in ['href', 'src']:
                    s += self.fix_url(val)
                else:
                    s += val
            s += '"'
        if closed:
            s += ' /'
        s += '>'

        if s:
            self.output.append(s)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        self.output.append('</' + tag + '>')

    def handle_data(self, data):
        self.output.append(data)

    def handle_charref(self, name):
        self.output.append('&#' + name + ';')

    def handle_entityref(self, name):
        self.output.append('&' + name + ';')

    def transform(self, text):
        self.feed(text)
        output = ''.join(self.output)
        self.output = []
        return output


def translate_site(url, text):
    text = LinkFixer(url).transform(text)
    return Translator([], ['html', 'zombie']).translate_string(text)


def translate_text(text):
    return Translator([], ['zombie']).translate_string(text)
