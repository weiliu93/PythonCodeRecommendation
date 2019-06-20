from pcr.storage.append_only_array_storage import AppendOnlyArrayStorage


class CorpusWriter(object):
    def __init__(self, storage_filepath, flush=False):
        self._storage = AppendOnlyArrayStorage(storage_filepath, flush)

    def write_corpus(self, code, features, filepath):
        """
        very straightforward solution now...
        """
        self._storage.append({
            "code": code,
            "features": features,
            "filepath": filepath
        })

    def close(self):
        self._storage.close()