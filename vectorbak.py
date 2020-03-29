#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
- 实现基本模拟数字类型
- 实现了切片功能：__len__ 和 __getitem__，这两个方法也是 vector 表现为序列所必需的
  若使用 [1:4]，返回的是 slice ，slice 是内置的类型，通过审查 slice ，
  发现它有 start,stop和step 数据属性，以及 indices 方法。indices 中，
  给定长度为 len 的序列，计算 s 标识的扩展切片的起始和结束索引，以及步幅，超过边界的索引会被截掉。
- 动态存取属性：__getattr__ 和 __setattr__ ,前者是为了获取 vector 分量，后者是对已有分量的保护，
  v.x 不可以直接赋值，因为 x已经成为v的属性了，v.x 的值改变了，但是v的值未改变。
- 散列和快速等值测试：__hash__
- 格式化：__format__

# @File : vector.py
# @Time : 2020/3/27 19:28 
# @GitHub: https://github.com/hittun/vector
"""
from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools


class Vector(object):
    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, *components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __gt__(self, other):
        """>"""
        if len(self) == len(other):
            cnt = len(self)
            index_max = max(0, cnt - 1)
            for a, b in zip(self, other):
                if a < b:
                    return False
            return self[index_max] != other[index_max]

    def __lt__(self, other):
        """<"""
        cnt = len(self)
        index_max = max(0, cnt - 1)
        for a, b in zip(self, other):
            if a > b:
                return False
        return self[index_max] != other[index_max]

    def __ge__(self, other):
        """>="""
        if len(self) == len(other):
            for a, b in zip(self, other):
                if a < b:
                    return False
            return True

    def __le__(self, other):
        """<="""
        if len(self) == len(other):
            for a, b in zip(self, other):
                if a > b:
                    return False
            return True

    def __eq__(self, other):
        """=="""
        return (len(self) == len(other) and
                all(a == b for a, b in zip(self, other)))

    def __ne__(self, other):
        """!="""
        return not __eq__(other)

    def __add__(self, other):
        """+"""
        if len(self) == len(other):
            cls = type(self)
            new = [a + b for a, b in zip(self, other)]
            return cls(*new)

    def __sub__(self, other):
        """-"""
        if len(self) == len(other):
            cls = type(self)
            new = [a - b for a, b in zip(self, other)]
            return cls(*new)

    def __hash__(self):
        hashes = (hash(x) for x in self)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))

    # def __getattr__(self, name):
    #     cls = type(self)
    #     if len(name) == 1:
    #         pos = cls.shortcut_names.find(name)
    #         if 0 <= pos < len(self._components):
    #             return self._components[pos]
    #     msg = '{.__name__!r} object has no attribute {!r}'
    #     raise AttributeError(msg.format(cls, name))

    # def __setattr__(self, name, value):
    #     """protect attrs"""
    #     cls = type(self)
    #     if len(name) == 1:
    #         if name in cls.shortcut_names:
    #             error = 'readonly attribute {attr_name!r}'
    #         elif name.islower():
    #             error = "can't set attributes 'a' to 'z' in {cls_name!r}"
    #         else:
    #             error = ''
    #         if error:
    #             msg = error.format(cls_name=cls.__name__, attr_name=name)
    #             raise AttributeError(msg)
    #     super().__setattr__(name, value)

    # def __setattr__(self, name, value):
    #     cls = type(self)
    #     if len(name) == 1:
    #         pos = cls.shortcut_names.find(name)
    #         if 0 <= pos < len(self._components):
    #             self._components[pos] = value

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n - 1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # hyperspherical coordinates
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)],
                                     self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


class Vec2(Vector):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(x, y)


class Vec3(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z)


class Vec4(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0, t=0.0):
        super().__init__(x, y, z, t)


class VecFrame2(Vec2):
    shortcut_names = 'wh'


class VecFrame3(Vec3):
    shortcut_names = 'whd'



