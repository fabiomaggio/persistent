##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# Example objects for pickling.

from persistent import Persistent


def print_dict(d):
    d = d.items()
    d.sort()
    print '{%s}' % (', '.join(
        [('%r: %r' % (k, v)) for (k, v) in d]
        ))

def cmpattrs(self, other, *attrs):
    for attr in attrs:
        if attr[:3] in ('_v_', '_p_'):
            continue
        c = cmp(getattr(self, attr, None), getattr(other, attr, None))
        if c:
            return c
    return 0

class Simple(Persistent):
    def __init__(self, name, **kw):
        self.__name__ = name
        self.__dict__.update(kw)
        self._v_favorite_color = 'blue'
        self._p_foo = 'bar'

    def __cmp__(self, other):
        return cmpattrs(self, other, '__class__', *(self.__dict__.keys()))

class Custom(Simple):

    def __new__(cls, x, y):
        r = Persistent.__new__(cls)
        r.x, r.y = x, y
        return r

    def __init__(self, x, y):
        self.a = 42

    def __getnewargs__(self):
        return self.x, self.y

    def __getstate__(self):
        return self.a

    def __setstate__(self, a):
        self.a = a


class Slotted(Persistent):

    __slots__ = 's1', 's2', '_p_splat', '_v_eek'

    def __init__(self, s1, s2):
        self.s1, self.s2 = s1, s2
        self._v_eek = 1
        self._p_splat = 2


class SubSlotted(Slotted):

    __slots__ = 's3', 's4'

    def __init__(self, s1, s2, s3):
        Slotted.__init__(self, s1, s2)
        self.s3 = s3

    def __cmp__(self, other):
        return cmpattrs(self, other, '__class__', 's1', 's2', 's3', 's4')


class SubSubSlotted(SubSlotted):

    def __init__(self, s1, s2, s3, **kw):
        SubSlotted.__init__(self, s1, s2, s3)
        self.__dict__.update(kw)
        self._v_favorite_color = 'blue'
        self._p_foo = 'bar'

    def __cmp__(self, other):
        return cmpattrs(self, other,
                        '__class__', 's1', 's2', 's3', 's4',
                        *(self.__dict__.keys()))
