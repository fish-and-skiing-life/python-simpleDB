#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyByteBuffer import ByteBuffer
import sys
import math

class Page:
    CHARSET = 'us-ascii'
    INT_SIZE = 4
    def __init__(self, block):
        self._bb = None
        if type(block) is int:
            self._bb = ByteBuffer.allocate(block)
        else:
            self._bb = ByteBuffer.wrap(block)

    def get_int(self, offset):
        self._bb.position = offset
        return self._bb.get(Page.INT_SIZE)

    def set_int(self, offset, n):
        self._bb.position = offset
        self._bb.put(n, Page.INT_SIZE)

    def get_bytes(self, offset):
        self._bb.position = offset
        length = self._bb.get()
        return self._bb.get(length).to_bytes(length, 'big')

    def set_bytes(self, offset, b):
        self._bb.position = offset
        self._bb.put(len(b))
        self._bb.put(b)

    def get_string(self, offset):
        b = self.get_bytes(offset)
        return b.decode(self.CHARSET)

    def set_string(self, offset, s):
        b = s.encode(Page.CHARSET)
        self.set_bytes(offset, b)

    @staticmethod
    def max_length(strlen):
        # bytes_per_char = '-'.encode(Page.CHARSET)
        # return sys.getsizeof(int) + (strlen * sys.getsizeof(bytes_per_char))
        return Page.int_size(strlen) + strlen

    def contents(self):
        self._bb.rewind()
        return self._bb.buffer

    def bb_to_str(self):
        return '[ position: '+str(self._bb.position)+', remaining: '+str(self._bb.remaining)+', buffer: '+self._bb.buffer.decode(Page.CHARSET)+' ]'

    @staticmethod
    def int_size(i):
        """
        return the number of bytes occupied by `i`
        PyByteBuffer > utilsから取ってきた
        """
        if i == 0:
            return 1
        return int(math.log(i, 256)) + 1


if __name__ == '__main__':
    p1 = Page(400)
    pos1 = 88
    p1.set_string(pos1, 'abcdefghijklmnopqrstuvwxyzzzzzzzzzzzzzzzzzz')
    print(p1.get_string(88))
    size = Page.max_length(len("abcdefghijklmnopqrstuvwxyzzzzzzzzzzzzzzzzzz"))
    pos2 = pos1 + size
    p1.set_int(pos2, 2147483647)
    print(p1.get_int(pos2))

