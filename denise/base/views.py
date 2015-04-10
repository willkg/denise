import urlparse

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from dennis.linter import Linter
from dennis.templatelinter import TemplateLinter
from dennis.tools import withlines
import polib
import requests

from denise.base.utils import translate_site, translate_text


def index_view(request):
    error = ''
    text = ''
    translatedstring = ''

    try:
        if request.GET.get('urltotranslate'):
            # FIXME: This should be a different url.
            # Translate a url
            url = request.GET.get['urltotranslate']
            print url
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            parts = urlparse.urlparse(url)
            if parts.scheme in ('http', 'https') and parts.netloc:
                resp = requests.get(url)
                return translate_site(url, resp.text)

        elif request.GET.get('text'):
            # FIXME: This should be an API.
            # Translate a string
            text = request.GET.get('text', '')
            translatedstring = translate_text(text)

    except Exception as exc:
        print exc
        error = 'cough'

    return render(request, 'index.html', context={
        'error': error,
        'text': text,
        'translatedstring': translatedstring,
        'urltotranslate': request.GET.get('urltotranslate', '')
    })


# FIXME: rewrite
def lint_view(request):
    # FIXME: Test POST
    upload = request.files['pofile']
    if not upload:
        return HttpResponseRedirect(reverse('index-view'))

    results = []
    metadata = []
    calculateddata = []
    error = ''
    filename = upload.filename

    if not upload.filename.endswith(('.po', '.pot')):
        error = '%s is not an acceptable file .po and .pot files only..' % upload.filename

    else:
        is_po = filename.endswith('.po')

        contents = upload.stream.read().decode('utf-8')
        # Get metadata from the pofile so we can print it out for some
        # context.
        po = polib.pofile(contents)

        for key, val in po.metadata.items():
            if isinstance(val, str):
                val = val.decode('utf-8')

            metadata.append((key, val))

        if is_po:
            calculateddata.append(('Percent translated', str(po.percent_translated())))

            # FIXME: Hard-coded
            linter = Linter(['pysprintf', 'pyformat'], [])
        else:
            # FIXME: Hard-coded
            linter = TemplateLinter(['pysprintf', 'pyformat'], [])

        results = linter.verify_file(contents)

    # FIXME: We should move this somewhere else?
    def entry_with_lines(poentry):
        return withlines(poentry.linenum, poentry.original).splitlines(True)

    return render(request, 'lint.html', context={
        'error': error,
        'metadata': metadata,
        'calculateddata': calculateddata,
        'warn_results': [res for res in results if res.kind == 'warn'],
        'err_results': [res for res in results if res.kind == 'err'],
        'filename': filename,
        'entry_with_lines': entry_with_lines
    })
