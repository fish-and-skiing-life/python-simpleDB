import sys
sys.path.append("../file_manager")
from page import Page
from block_id import BlockId
from file_mgr import FileMgr

class LogIterator:
    def __init__(self, fm: FileMgr, blk: BlockId):
        self._fm = fm
        self._blk = blk
        self._p = Page(fm.block_size())
        self._currentpos = 0
        self._boundary = 0
        self._move_to_block(blk)

    def __iter__(self):
        return self

    def has_next(self) -> bool:
        return self._currentpos < self._fm.block_size() or self._blk.number() > 0

    def __next__(self):
        if self._currentpos == self._fm.block_size():
            self._blk = BlockId(self._blk.filename(), self._blk.number()-1)
            self._move_to_block(self._blk)
        rec = self._p.get_bytes(self._currentpos)
        self._currentpos += Page.INT_SIZE + len(rec)
        return rec

    def _move_to_block(self, block: BlockId):
        self._fm.read(block, self._p)
        self._boundary = self._p.get_int(0)
        self._currentpos = self._boundary
