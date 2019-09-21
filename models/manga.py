#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .model import Model


class Manga(Model):
    _title = None
    _link = None
    _is_completed = None

    def __init__(self, title, link, is_completed):
        self._title = title
        self._link = link
        self._is_completed = is_completed

    @property
    def title(self):
        return self._title

    @property
    def link(self):
        return self._link

    @property
    def is_completed(self):
        return self._is_completed

    @property
    def chapters(self):
        return self._items

    @chapters.setter
    def chapters(self, chapters):
        self._items = chapters

