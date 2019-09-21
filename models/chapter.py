#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Chapter(object):
    _manga = None
    _link = None
    _number = None
    _title = None
    _pages = []

    def __init__(self, manga, link, number, title):
        self._manga = manga
        self._link = link
        self._number = number
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
        return self._pages

    @pages.setter
    def pages(self, pages):
        self._pages = pages
