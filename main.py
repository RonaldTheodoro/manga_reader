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
    _mangas_dir = os.path.join(BASE_DIR, 'mangas')

    _mangas = []

    def __init__(self, **kwargs):
        if 'mangas_dir' in kwargs:
            self._mangas_dir = kwargs['mangas_dir']
        self._create_directory(self._mangas_dir)

    def _create_directory(self, directory):
        """Checks if a directory exists and if not create it.

        Args:
            directory (str): Directory path.
        """
        if not os.path.exists(directory):
            os.mkdir(directory)

    def download_mangas(self):
        """Download the mangas.
        """
        pass

    @property
    def mangas(self):
        """Return a list with all mangas avabile,

        Returns:
            list[models.Mangas]: List of mangas.
        """
        if not self._mangas:
            response = self.get_page(self.URL_LIST)

            self._parsing_mangas(response)

        return self._mangas

    def get_page(self, url):
        """Make a request and return the site response.

        Args:
            url (str): URL page

        Returns:
            requests.models.Response: Page response.
        """
        response = self.session.get(url)
        response.raise_for_status()
        return response

        """Parsing all mangas links.

        Args:
            response (requests.models.Response): Page response.
        """
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
