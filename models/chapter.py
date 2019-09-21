#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Chapter(object):
    _link = None
    _number = None
    _title = None
    _pages = []

    def __init__(self, link, number, title):
        self._link = link
        self._number = number
        self._title = title

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
