from pcr.storage.append_only_array_storage import AppendOnlyArrayStorage

class IndexWriter(object):

    def __init__(self, storage_filepath):
        self._storage = AppendOnlyArrayStorage(storage_filepath)

    def write(self, features, line_number, next_line):
        self._storage.append({
            "features": features,
            "line_number": line_number,
            "next_line": next_line
        })

    def close(self):
        self._storage.close()