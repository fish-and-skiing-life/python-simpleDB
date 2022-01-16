#!/usr/bin/python
# -*- coding: utf-8 -*-

class BlockId:
    def __init__(self, filename, blknum):
        self._filename = filename
        self._blknum = blknum

    def filename(self):
        return self._filename

    def number(self):
        return self._blknum

    def __eq__(self, obj):
        return self._filename == obj.filename() and self._blknum == obj.number()

    def __str__(self):
        return '[file ' + self._filename + ', block ' + str(self._blknum) + ']'

    def __hash__(self):
        return hash(str(self))

"""
実行サンプル
>>> from block_id import BlockId
>>> a = BlockId('hoge', 3)
>>> b = BlockId('hoge', 2)
>>> print(a)
[file hoge, block 3]
>>> print(b)
[file hoge, block 2]
>>> print(a == b)
False
>>> c = BlockId('hoge', 3)
>>> print(a == c)
True
>>> print(a is c)
False
>>>
"""