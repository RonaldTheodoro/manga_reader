#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib

import lxml.html
import requests
from betamax import Betamax
from betamax_serializers import pretty_json

import models

WORKERS_DIR = os.path.dirname(os.path.abspath(__file__))
CASSETTES_DIR = os.path.join(WORKERS_DIR, u'resources', u'cassettes')
MATCH_REQUESTS_ON = [u'method', u'uri', u'path', u'query']

Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
with Betamax.configure() as config:
    config.cassette_library_dir = CASSETTES_DIR
    config.default_cassette_options[u'serialize_with'] = u'prettyjson'
    config.default_cassette_options[u'match_requests_on'] = MATCH_REQUESTS_ON
    config.default_cassette_options[u'preserve_exact_body_bytes'] = True


class MangaReaderWorker(object):
    session = requests.Session()

    URL_BASE = u'https://www.mangareader.net'
    URL_LIST = urllib.parse.urljoin(URL_BASE, 'alphabetical')

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MANGAS_DIR = os.path.join(BASE_DIR, 'mangas')

    _mangas = []

    def __init__(self):
        self._create_directory(self.MANGAS_DIR)

    def _create_directory(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

    def download_mangas(self):
        pass

    @property
    def mangas(self):
        if not self._mangas:
            response = self.get_page(self.URL_LIST)

            self._parsing_mangas(response)

        return self._mangas

    def get_page(self, url):
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def _parsing_mangas(self, response):
        root = lxml.html.fromstring(response.content, base_url=self.URL_BASE)
        root.make_links_absolute()

        for manga in root.xpath('//ul[@class="series_alpha"]/li')[:2]:
            link, = manga.xpath('./a')

            if manga.xpath('./span[contains(text(), "Completed")]'):
                is_completed = True
            else:
                is_completed = False

            manga_obj = models.Manga(
                title=link.text_content().strip(),
                link=link.get('href'),
                is_completed=is_completed,
            )
            self._mangas.append(manga_obj)


if __name__ == "__main__":
    worker = MangaReaderWorker()
    with Betamax(worker.session) as vcr:
        vcr.use_cassette(u'manga_list')
        worker.download_mangas()
