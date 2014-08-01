import HTMLParser
import urlparse

from flask import Blueprint, render_template, request

import polib
import requests

from dennis.linter import Linter
from dennis.translator import Translator


mod = Blueprint('main', __name__)


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


def zombie_site(url):
    resp = requests.get(url)
    text = LinkFixer(url).transform(resp.text)
    return Translator([], ['html', 'zombie']).translate_string(text)


def zombie_text(text):
    return Translator([], ['zombie']).translate_string(text)


@mod.route('/lint', methods=['POST'])
def lint():
    upload = request.files['pofile']
    if not upload:
        # Send them away
        pass

    results = []
    metadata = []
    calculateddata = []
    error = ''
    filename = upload.filename

    if not upload.filename.endswith('.po'):
        error = '%s is not an acceptable file.' % upload.filename

    else:
        contents = upload.stream.read()

        # Get metadata from the pofile so we can print it out for some
        # context.
        po = polib.pofile(contents)

        lang = ''
        for key, val in po.metadata.items():
            if key == 'Language':
                lang = val

            if isinstance(val, str):
                val = val.decode('utf-8')

            metadata.append((key, val))

        calculateddata.append(('Percent translated', str(po.percent_translated())))

        if lang:
            calculateddata.append(('Verbatim link', 'https://localize.mozilla.org/%s/sumo/' % lang))

        # FIXME: Hard-coded
        linter = Linter(['pysprintf', 'pyformat'], [])

        results = linter.verify_file(contents)

        lint_results = [r for r in results if r.has_problems()]

    return render_template(
        'lint.html',
        error=error,
        metadata=metadata,
        calculateddata=calculateddata,
        results=lint_results,
        filename=filename,
        zip=zip  # Need this function in the template
    )


@mod.route('/')
def index():
    error = ''
    text = ''
    translatedstring = ''

    try:
        if request.args.get('url'):
            # Zombify a url
            url = request.args['url']
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            parts = urlparse.urlparse(url)
            if parts.scheme in ('http', 'https') and parts.netloc:
                return zombie_site(url)

        elif request.args.get('text'):
            # Zombify a string
            text = request.args['text']
            translatedstring = zombie_text(text)

    except Exception as exc:
        print exc
        error = 'cough'

    return render_template(
        'index.html',
        error=error,
        text=text,
        translatedstring=translatedstring,
        url=request.args.get('url')
    )
