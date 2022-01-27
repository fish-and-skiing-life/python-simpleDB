import os
import inspect
import threading
import ctypes
import copy

from block_id import BlockId
from page import Page
class FileMgr:
  def __init__(self, db_directory, blocksize):
    self._db_directory = db_directory
    self._blocksize = blocksize
    self._is_new = not os.path.isdir(db_directory)
    self._lock = threading.Lock()
    if self._is_new:
      os.mkdir(self._db_directory)

    for filename in os.listdir(self._db_directory):
      if filename.startswith("temp"):
        file_path = os.path.join(self._db_directory, filename)
        os.remove(file_path)

  def get_file(self, filename):
    file_path = os.path.join(self._db_directory, filename)
    if not os.path.isfile(file_path):
      return open(file_path, "w+b")
    else:
      return open(file_path, "r+b")

  def read(self, blk, page):
    with self._lock:
      try:
        f = self.get_file(blk.filename())
        f.seek(blk.number() * self._blocksize)
        page._bb.buffer = f.read()
        f.close()

      except OSError as e:
        raise ("cannot read block " + blk)

  def write(self, block, page):
    with self._lock:
      try:
        f = self.get_file(blk.filename())
        f.seek(blk.number() * self._blocksize)
        f.write(page.contents())
        f.close()
      except OSError as e:
        raise ("cannot read block " + blk)


  def append(self, filename):
    with self._lock:
      try:
        newblknum = self.length(filename)
        block = BlockId(filename, newblknum)
        # 空のbite配列の作成
        bytes_list = bytes(newblknum)
        f = self.get_file(block.filename())
        f.seek(block.number() * self._blocksize)
        f.write(bytes_list)
        f.close()
      except OSError as e:
        raise ("cannot append block " + filename)

      self._lock.release()

  def length(self, filename):
    try:
       f = self.get_file(filename)
       return int((f.length() / self._blocksize))
    except OSError as e:
       raise ("cannot access " + filename)

  def in_new(self):
    return self._is_new

  def block_size(self):
    return self._blocksize


if __name__ == '__main__':
  fm = FileMgr('fileset', 400)
  blk = BlockId('testfile', 2)
  p1 = Page(fm.block_size())
  pos1 = 88
  p1.set_string(pos1, "abcdefghijklm")
  size = Page.max_length(len("abcdefghijklm"))
  pos2 = pos1 + size
  p1.set_int(pos2, 345)
  fm.write(blk, p1)
  p2 = Page(fm.block_size())
  fm.read(blk, p2)
  print("offset " + str(pos2) +  " contains " + str(p2.get_int(pos2)))
  print("offset " + str(pos1) +  " contains " + p2.get_string(pos1))

  # public synchronized void write(BlockId blk, Page p) {
  #   try {
  #     RandomAccessFile f = getFile(blk.fileName());
  #     f.seek(blk.number() * blocksize);
  #     f.getChannel().write(p.contents());
  #   }
  #   catch (IOException e) {
  #     throw new RuntimeException("cannot write block" + blk);
  #   }
  # }

  # public synchronized BlockId append(String filename) {
  #   int newblknum = size(filename);
  #   BlockId blk = new BlockId(filename, newblknum);
  #   byte[] b = new byte[blocksize];
  #   try {
  #     RandomAccessFile f = getFile(blk.fileName());
  #     f.seek(blk.number() * blocksize);  f.write(b);
  #   }
#  private RandomAccessFile getFile(String filename)  throws IOException {  RandomAccessFile f = openFiles.get(filename);  if (f == null) {  File dbTable = new File(dbDirectory, filename);  f = new RandomAccessFile(dbTable, "rws");  openFiles.put(filename, f);  }  return f;  }