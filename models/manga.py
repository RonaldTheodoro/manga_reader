#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Manga(object):
    _title = None
    _link = None
    _is_completed = None
    _chapters = []

    def __init__(self, title, link, is_completed):
        self._title = title
        self._link = link
        self._is_completed = is_completed

    def __repr__(self):
        attrs = []
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                key = key.strip('_')
                attrs.append(f'{key}={value}')
        return f'<{self.__class__.__name__}({attrs})>'

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
        return self._chapters

    def download_chapters(self):
        raise NotImplemented