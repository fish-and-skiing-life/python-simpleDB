#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyByteBuffer import ByteBuffer
import sys
import inspect

class Page:
    CHARSET = 'us-ascii'
    def __init__(self, block):
        self._bb = None
        if type(block) is int:
            self._bb = ByteBuffer.allocate(block)
        else:
            self._bb = ByteBuffer.wrap(block)

    def get_int(self, offset):
        self._bb.position = offset
        return self._bb.get()

    def set_int(self, offset, n):
        self._bb.put(offset, n)

    def get_bytes(self, offset):
        self._bb.position = offset
        print('4. ' + str(self._bb))
        length = self._bb.get()
        b = bytes(length)
        print(self._bb.get(length))
        return b

    def set_bytes(self, offset, b):
        # self._bb._update_offsets(offset)
        self._bb.position = offset
        print('1. ' +  str(self._bb))
        self._bb.put(len(b))
        print('2. ' +  str(self._bb))
        self._bb.put(b)
        print('3. ' +  str( self._bb))

    def get_string(self, offset):
        b = self.get_bytes(offset)
        return b.decode(self.CHARSET)

    def set_string(self, offset, s):
        b = s.encode(Page.CHARSET)
        self.set_bytes(offset, b)
        print(self._bb)

    @staticmethod
    def max_length(strlen):
        bytes_per_char = '-'.encode(Page.CHARSET)
        return sys.getsizeof(int) + (strlen * sys.getsizeof(bytes_per_char))

    def contents(self):
        self._bb.rewind()
        return self._bb

if __name__ == '__main__':
    p1 = Page(400)
    pos1 = 88
    p1.set_string(pos1, 'abcdefghijklmn')
    print(p1.get_string(88))
    # size = Page.max_length(len("abcdefghijklm"))
    # pos2 = pos1 + size
    # p1.set_int(pos2, 345)

'''
これをByteBufferに書き込む

def __str__(self):
        return '[ position: '+str(self.position)+', remaining: '+str(self.remaining)+', buffer: '+self.buffer.decode()+' ]'

'''