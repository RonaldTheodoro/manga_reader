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
        self._number = int(number)
        self._title = title

    def __repr__(self):
        attrs = []
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                key = key.strip('_')
                attrs.append(f'{key}={value}')
        return f'{self.__class__.__name__}({", ".join(attrs)})'

    def __len__(self):
        return len(self._pages)

    def __getitem__(self, position):
        return self._pages[position]

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
