from pcr.util.bytes_util import byte_array_to_integer
from pcr.util.bytes_util import integer_to_byte_array

import pickle
import threading
import os
import mmap


class AppendOnlyArrayStorage(object):
    """append only array based in disk, thread safe"""

    def __init__(self, filepath, flush=False):
        self._filepath = filepath
        self._index_filepath = filepath + ".index"
        # overwrite current file
        if flush:
            open(self._filepath, "wb").close()
            open(self._index_filepath, "wb").close()
        # open data file and index file
        self._file = open(self._filepath, "ab")
        self._index_file = open(self._index_filepath, "ab")
        # offsets in-memory
        self._current_offset = self._file.tell()
        self._offsets = []
        self._load_index()
        self._lock = threading.Lock()

    def append(self, obj):
        self._lock.acquire()
        try:
            byte_array = self._serialize(obj)
            byte_array_length = len(byte_array)
            # write to disk first
            self._file.write(byte_array)
            self._index_file.write(integer_to_byte_array(self._current_offset, 4))
            # then update index in-memory
            self._offsets.append(self._current_offset)
            self._current_offset += byte_array_length
        finally:
            self._lock.release()

    def flush(self):
        self._lock.acquire()
        try:
            self._file.flush()
            self._index_file.flush()
        finally:
            self._lock.release()

    def close(self):
        self._lock.acquire()
        try:
            self._file.close()
            self._index_file.close()
        finally:
            self._lock.release()

    def __iter__(self):
        # flush data before iter
        self.flush()
        m = mmap.mmap(os.open(self._filepath, os.O_RDWR), 0)
        # sequence read without seeking
        # with open(self._filepath, "rb") as f:
        for index in range(len(self._offsets)):
            data_length = (
                self._offsets[index + 1] - self._offsets[index]
                if index + 1 < len(self._offsets)
                else self._current_offset - self._offsets[-1]
            )
            byte_array = m.read(data_length)
            yield self._deserialize(byte_array)
        m.close()

    def __len__(self):
        return len(self._offsets)

    def __getitem__(self, item):
        assert isinstance(item, int)
        assert item >= 0 and item < len(self._offsets), "index out of bound"
        # flush data first
        self.flush()
        # decide item start offset and data length
        start_offset = self._offsets[item]
        if item + 1 < len(self._offsets):
            data_length = self._offsets[item + 1] - start_offset
        else:
            data_length = self._current_offset - start_offset
        # seek for read once
        with open(self._filepath, "rb") as f:
            f.seek(start_offset)
            byte_array = f.read(data_length)
            return self._deserialize(byte_array)

    def _load_index(self):
        if os.stat(self._index_filepath).st_size > 0:
            # load index file in-memory
            m = mmap.mmap(os.open(self._index_filepath, os.O_RDWR), 0)
            # with open(self._index_filepath, "rb") as f:
            byte_array = m.read(4)
            while len(byte_array) == 4:
                integer = byte_array_to_integer(byte_array)
                self._offsets.append(integer)
                byte_array = m.read(4)
            m.close()

    def _serialize(self, obj):
        return pickle.dumps(obj)

    def _deserialize(self, byte_array):
        return pickle.loads(byte_array)
