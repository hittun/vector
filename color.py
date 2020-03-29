#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# Color with RGBA
# @File : color.py
# @Time : 2020/3/27 19:01 
# @GitHub: https://github.com/hittun/pygamel
"""


class Color(object):
    MAX = 255
    MIN = 0

    shortcut_names = 'rgba'

    def __init__(self, components):
        cls = type(self)
        cnt = len(components)
        if cnt < 1 or cnt > 3:
            msg = '{.__name__!r} attribute count error {!r}'
            raise AttributeError(msg.format(cls, components))
        for index in range(len(cls.shortcut_names)):
            key = cls.shortcut_names[index]
            value = cls.MAX if cnt < index+1 else components[index]
            self.__setattr__(key, value)

    def __setattr__(self, name, value):
        cls = type(self)
        if name in cls.shortcut_names:
            if value > cls.MAX:
                value = cls.MAX
            elif value < cls.MIN:
                value = cls.MIN
            super().__setattr__(name, int(value))
        else:
            msg = '{.__name__!r} attribute name error {!r}'
            raise AttributeError(msg.format(cls, name))

    def __repr__(self):
        cls = type(self)
        components = []
        for key in cls.shortcut_names:
            components.append(getattr(self, key))
        return 'Color{}'.format(tuple(components))


