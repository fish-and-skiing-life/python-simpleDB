#!/usr/bin/python
# -*- coding: utf-8 -*-

from file.page import Page
from file.block_id import BlockId
from file.file_mgr import FileMgr

class LogIterator:
    def __init__(self, fm: FileMgr, blk: BlockID):
        self._fm = fm
        self._blk = blk
        self._p = Page(fm.blockSize())
        self._currentpos = 0
        self._boundary = 0
        self._move_to_block(blk)

    def __iter__(self):
        return self

    def has_next(self) -> bool:
        return self._currentpos < self._fm.blockSize() or self._blk.number() > 0

    def __next__(self):
        if self._currentpos == self._fm.blockSize():
            self._blk = BlockId(self._blk.filename(), self._blk.number()-1)
            self._move_to_block(blk)
        rec = self._p.get_bytes(self._currentpos)
        self._currentpos += Page.INT_SIZE + len(rec)

    def _move_to_block(self, block: blockID):
        fm.read(blk, self._p)
        self._boundary = p.get_int(0)
        self._currentpos = self._boundary
