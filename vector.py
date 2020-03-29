#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @File : vector.py
# @Time : 2020/3/28 0:20 
# @GitHub: https://github.com/hittun/pygamel
"""
import sys
import math


class Vector(object):
    shortcut_names = 'xyzabcdefghijklmnopqrstuvw'
    _keys = set()

    def __init__(self, *args, **kwargs):
        cls = type(self)
        for pos in range(len(args)):
            name = cls.shortcut_names[pos]
            value = args[pos]
            self.__setattr__(name, value)
        for name, value in kwargs.items():
            self.__setattr__(name, value)

    # def __getattr__(self, item):
    #     item = item.lower()
    #     if item in self.__dict__:
    #         return self.__dict__[item]

    def __setattr__(self, key, value):
        if isinstance(key, str):
            key = key.lower()
            cls = type(self)
            if key in cls.shortcut_names:
                self._keys.add(key)
                super().__setattr__(key, value)
            else:
                msg = '{}::{} key not in shortcut_names'
                raise TypeError(msg.format(self.__class__.__name__, sys._getframe().f_code.co_name))
        else:
            msg = '{}::{} key must be str'
            raise TypeError(msg.format(self.__class__.__name__, sys._getframe().f_code.co_name))

    def __delattr__(self, item):
        self._keys.discard(item)
        super().__delattr__(item)

    def keys(self):
        return self._keys

    def sortedkeys(self):
        cls = type(self)
        keys = list(self.keys())
        keys.sort(key=lambda x: cls.shortcut_names.index(x))
        return keys

    def dict(self):
        return {k: getattr(self, k, None) for k in self.keys()}

    def items(self):
        return self.dict().items()

    def default(self):
        cls = type(self)
        for k in cls.shortcut_names:
            self.__setattr__(k, 0.0)

    def __len__(self):
        return len(self.keys())

    def __sizeof__(self):
        return len(self.keys())

    def __str__(self):
        return str(self.dict())

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        """>"""
        keys = self.sortedkeys()
        if len(self) == len(other):
            a, b = 0, 0
            for k in keys:
                a = self.__getattribute__(k)
                b = other.__getattribute__(k)
                if a < b:
                    return False
            return a != b

    def __lt__(self, other):
        """<"""
        keys = self.sortedkeys()
        if len(self) == len(other):
            a, b = 0, 0
            for k in keys:
                a = self.__getattribute__(k)
                b = other.__getattribute__(k)
                if a > b:
                    return False
            return a != b

    def __ge__(self, other):
        """>="""
        keys = self.sortedkeys()
        if len(self) == len(other):
            for k in keys:
                a = self.__getattribute__(k)
                b = other.__getattribute__(k)
                if a < b:
                    return False
            return True

    def __le__(self, other):
        """<="""
        keys = self.sortedkeys()
        if len(self) == len(other):
            for k in keys:
                a = self.__getattribute__(k)
                b = other.__getattribute__(k)
                if a > b:
                    return False
            return True

    def __eq__(self, other):
        """=="""
        keys = self.sortedkeys()
        if len(self) == len(other):
            all(self.__getattribute__(k) == other.__getattribute__(k) for k in keys)

    def __ne__(self, other):
        """!="""
        return not __eq__(other)

    def __add__(self, other):
        """后操作有可能改变类型：cls = type(other)，类似a = 1 , b = 1.0 , a + b = 2.0"""
        """+"""
        if len(self) == len(other):
            temp = {}
            for key in self.keys() | other.keys():
                a = getattr(self, key, 0)
                b = getattr(other, key, 0)
                temp[key] = a + b
            cls = type(other)
            return cls(**temp)

    def __sub__(self, other):
        """后操作有可能改变类型：cls = type(other)，类似a = 1 , b = 1.0 , a - b = 0.0"""
        """-"""
        if len(self) == len(other):
            temp = {}
            for key in self.keys() | other.keys():
                a = getattr(self, key, 0)
                b = getattr(other, key, 0)
                temp[key] = a - b
            cls = type(other)
            return cls(**temp)

    def __abs__(self):
        keys = self.sortedkeys()
        return math.sqrt(sum(self.__getattribute__(x) * self.__getattribute__(x) for x in keys))

    def __bool__(self):
        return bool(abs(self))


class Vec2(Vector):
    shortcut_names = 'xy'

    def __init__(self, *args, **kwargs):
        self.default()
        super().__init__(*args, **kwargs)


class Vec3(Vector):
    shortcut_names = 'xyz'

    def __init__(self, *args, **kwargs):
        self.default()
        super().__init__(*args, **kwargs)


class VecFrame2(Vec2):
    shortcut_names = 'wh'


class VecFrame3(Vec3):
    shortcut_names = 'whd'