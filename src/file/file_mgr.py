import os
import inspect
import threading
import ctypes

from block_id import BlockId
from page import Page
class FileMgr:
  def __init__(self, dbDirectory, blocksize):
    self._dbDirectory = dbDirectory;
    self._blocksize = blocksize;
    self._isNew = not os.path.isdir(dbDirectory)
    self._lock = threading.Lock()
    if self._isNew:
      os.mkdir(self._dbDirectory)

    for filename in os.listdir(self._dbDirectory):
      if filename.startswith("temp"):
        file_path = os.path.join(self._dbDirectory, filename)
        os.remove(file_path)

  def getFile(self, filename):
    file_path = os.path.join(self._dbDirectory, filename)
    return open(file_path, "w+")

  def read(self, blk, page):
    with self._lock:
      try:
        self._lock.acquire()
        f = self.getFile(blk.filename())
        f.seek(blk.number() * self._blocksize)
        f.read( id((page.contents().copy())[0]))


        f.close()
        # memset(&((*page.contents())[readCount]),  0, block_size_ - readCount);

      except OSError as e:
        raise ("cannot read block " + blk)

      self._lock.release()

  def write(self, block, page):
    with self._lock:
      try:
        self._lock.acquire()
        f = self.getFile(blk.filename())
        f.seek(blk.number() * self._blocksize)
        f.write(id((page.contents().copy())[0]))
        f.close()
      except OSError as e:
        raise ("cannot read block " + blk)

      self._lock.release()

  def inNew(self):
    return self._isNew

  def blockSize(self):
    return self._blocksize


fm = FileMgr('fileset', 400)
a = BlockId('testfile', 2)
p1 = Page(fm.blockSize());
pos1 = 88;
p1.set_string(pos1, "abcdefghijklm");
size = Page.max_length("abcdefghijklm".length());
pos2 = pos1 + size;  p1.set_int(pos2, 345);
fm.write(blk, p1);
p2 = nPage(fm.blockSize());
fm.read(blk, p2);
print("offset " + pos2 +  " contains " + p2.getInt(pos2));
print("offset " + pos1 +  " contains " + p2.getString(pos1));

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