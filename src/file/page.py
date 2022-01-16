#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyByteBuffer import ByteBuffer
import sys
import inspect

class Page:
    CHARSET = 'utf-8'
    def __init__(self, block):
        self._bb = None
        if type(block) is int:
            self._bb = ByteBuffer.allocate(block)
        else:
            self._bb = ByteBuffer.wrap(block)

    def get_int(self, offset):
        return self._bb.getInt(offset)

    def set_int(self, obj):
        self._bb.putInt(offset, n)

    def get_bytes(self, offset):
        self._bb.position(offset)
        length = self._bb.getInt()
        b = bytes(length)
        self._bb.get(b)
        return b

    def set_bytes(self, offset, b):
        self._bb.position(offset)
        self._bb.putInt(len(b))
        self._bb.put(b)

    def get_string(self, offset):
        b = self.get_bytes(offset)
        return b.decode(self.CHARSET)

    def set_string(self, offset, s):
        b = self.get_bytes(offset)
        self.set_bytes(offset, b)

    @staticmethod
    def max_length(strlen):
        sys.getsizeof(int) + (strlen * sys.getsizeof(str))

    def contents():
        bb.position(0)
        return self._bb