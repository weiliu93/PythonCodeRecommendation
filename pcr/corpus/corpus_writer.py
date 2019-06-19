from pcr.storage.append_only_array_storage import AppendOnlyArrayStorage


class CorpusWriter(object):
    def __init__(self, storage_filepath):
        self._storage = AppendOnlyArrayStorage(storage_filepath, flush=True)

    def write_corpus(self, code, features, filepath):
        """
        very straight solution now...
        """
        self._storage.append({
            "code": code,
            "features": features,
            "filepath": filepath
        })

    def close(self):
        self._storage.close()