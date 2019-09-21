#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Model(object):
    _items = []

    def __repr__(self):
        attrs = []
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                key = key.strip('_')
                attrs.append(f'{key}={value}')
        return f'{self.__class__.__name__}({", ".join(attrs)})'

    def __len__(self):
        return len(self._items)

    def __getitem__(self, position):
        return self._items[position]

    def path(self):
        raise NotImplementedError()
