#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from .model import Model


class Chapter(Model):
    _manga = None
    _link = None
    _number = None
    _title = None

    def __init__(self, manga, link, number, title):
        self._manga = manga
        self._link = link
        self._number = int(number)
        self._title = title

    @property
    def manga(self):
        return self._manga

    @property
    def link(self):
        return self._link

    @property
    def number(self):
        return self._number

    @property
    def title(self):
        return self._title

    @property
    def pages(self):
        return self._items

    @pages.setter
    def pages(self, pages):
        self._items = pages

    @property
    def path(self):
        return os.path.join(self.manga.path, str(self.number))
