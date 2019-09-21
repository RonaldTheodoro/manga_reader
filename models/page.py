#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils


class Page(object):
    _number = None
    _page_link = None
    _img_link = None
    _img_file = None

    def __init__(self, number, page_link, img_link=None, img_file=None):
        self._number = number

        if utils.is_url(page_link):
            self._page_link = page_link
        else:
            raise ValueError(f'{page_link} is not a valid url')

        if img_link is not None and utils.is_url(img_link):
            self._img_link = img_link

        if img_file is not None:
            self._img_file = img_file

    @property
    def number(self):
        return self._number

    @property
    def page_link(self):
        return self._page_link

    @property
    def img_link(self):
        return self._img_link

    @img_link.setter
    def img_link(self, img_link):
        if utils.is_url(img_link):
            self._img_link = img_link
        else:
            raise ValueError(f'{img_link} is not a valid url')

    @property
    def img_file(self):
        return self._img_file

    @img_file.setter
    def img_file(self, img_file):
        self._img_file = img_file
