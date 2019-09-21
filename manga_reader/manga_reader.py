#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib

import requests

import models
import utils


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
        utils.create_directory(self._mangas_dir)

    def download_mangas(self):
        """Download the mangas.
        """
        for manga in self.mangas:
            response = self._get_page(manga.link)
            manga.chapters = self._get_chapters(response)

    @property
    def mangas(self):
        """Return a list with all mangas avabile,

        Returns:
            list[models.Mangas]: List of mangas.
        """
        if not self._mangas:
            response = self._get_page(self.URL_LIST)

            self._parsing_mangas_links(response)

        return self._mangas

    def _get_page(self, url):
        """Make a request and return the site response.

        Args:
            url (str): URL page

        Returns:
            requests.models.Response: Page response.
        """
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def _parsing_mangas_links(self, response):
        """Parsing all mangas links.

        Args:
            response (requests.models.Response): Page response.
        """
        root = utils.create_html_element_instance(response, self.URL_BASE)

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

    def _get_chapters(self, response):
        root = utils.create_html_element_instance(response, self.URL_BASE)
        chapters = []
        for chapter in root.xpath('//table[@id="listing"]//tr[not(@class)]'):
            link, = chapter.xpath('.//a/@href')
            number = self._parsing_chapter_number(chapter, './/a/text()')
            title = self._parsing_chapter_title(
                chapter,
                './/td/text()[preceding-sibling::a]'
            )
            chapters.append(models.Chapter(link, number, title))
        return chapters

    def _parsing_chapter_number(self, chapter, xpath):
        """Parsing the chapter number.

        Args:
            chapter (lxml.html.HtmlElement): HTML Element.
            xpath (str): XPath expresion.

        Returns:
            int: Chapter number.
        """
        number, = chapter.xpath(xpath)
        chapter_number = re.search(r'(?P<number>\d+)$', number)
        return int(chapter_number.group('number'))

    def _parsing_chapter_title(self, chapter, xpath):
        """Parsing the chapter title.

        Args:
            chapter (lxml.html.HtmlElement): HTML Element.
            xpath (str): XPath expresion.

        Returns:
            str: Chapter title.
        """
        title, = chapter.xpath(xpath)
        chapter_title = re.search(r' : (?P<title>.*)', title)
        if not chapter_title.group('title'):
            return None
        return chapter_title.group('title')
