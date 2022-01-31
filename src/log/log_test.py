import sys
sys.path.append("../file_manager")

from log_mgr import LogMgr
from file_mgr import FileMgr
from page import Page

class LogTest:
  def __init__(self):
    fm = FileMgr('logtest', 400)
    self.lm = LogMgr(fm, 'simpledb.log')

    self.print_log_records("The initial empty log file:")
    print("done");
    self.create_records(1, 35);
    self.print_log_records("The log file now has these records:");
    self.create_records(36, 70);
    self.lm.flush(65);
    self.print_log_records("The log file now has these records:");

  def print_log_records(self, msg):
    print(msg)
    iterator = self.lm.iterator()
    while iterator.has_next():
      rec = next(iterator)
      p = Page(rec)
      s = p.get_string(0)
      npos = Page.max_length(s.length());
      val = p.get_int(npos)
      print('[' + s + ',' + val + ']')

    print()

  def create_records(self, start, end):
    print('Creating records: ')
    for i in range(start, end):
      rec = self.create_log_record('record'+str(i), i+100)
      lsn = self.lm.append(rec)
      print(lsn + ' ')

    print()

  def create_log_record(self, s, n):
    spos = 0
    npos = spos + Page.max_length(s.length())
    b = bytearray(npos + Page.INT_SIZE)
    p = Page(b)
    p.set_string(spos, s)
    p.set_int(npos, n)
    return b


LogTest()