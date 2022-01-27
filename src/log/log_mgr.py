import sys
import threading

sys.path.append("../file_manager")
from block_id import BlockId
from file_mgr import FileMgr
from page import Page
from log_iterator import LogIterator

class LogMgr:
  def __init__(self, fm, logfile):
    self._fm = fm
    self._logfile = logfile
    self._latest_lsn = 0
    self._last_saved_lsn = 0
    byte_list = bytearray(fm.block_size())
    self._logpage = Page(byte_list)
    self._lock = threading.Lock()

    logsize = fm.length(logfile)
    if self._logfile == 0:
      self._current_block = append_new_block()
    else:
      self._current_block = BlockId(logfile, logsize - 1)
      fm.read(self._current_block, self._logpage)

  def flush(self, lsn):
    if lsn >= self._last_saved_lsn:
       self._flush();

  def append(self, logrec):
    with self._lock:
      boundary = self._logpage.get_int(0)
      recsize = logrec.length
      bytesneeded = recsize + Page.INT_SIZE
      if boundary - bytesneeded < Page.INT_SIZE:
        self._flush()
        currentblk = append_new_block();
        boundary = self._logpage.get_int(0)

      recpos = boundary - bytesneeded

      self._logpage.set_bytes(recpos, logrec)
      self._logpage.set_int(0, recpos)
      self._latest_lsn += 1
      return self._latest_lsn

  def append_new_block(self):
    blk = self._fm.append(self._logfile)
    self._logpage.set_int(0, self._fm.block_size())
    self._fm.write(blk, self._logpage);
    return blk;

  def iterator(self):
    self._flush()
    return LogIterator(self._fm, self._current_block)

  def _flush(self):
    self._fm.write(self._current_block, self._logpage)
    self._last_saved_lsn = self._latest_lsn
