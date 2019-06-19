from pcr.storage.append_only_array_storage import AppendOnlyArrayStorage


class CorpusReader(object):

    def __init__(self, storage_filepath):
        self._storage = AppendOnlyArrayStorage(storage_filepath)

    def __iter__(self):
        for dict_item in self._storage:
            # since we use dict as item storage, double check item type here
            if isinstance(dict_item, dict):
                yield dict_item["code"], dict_item["features"], dict_item["filepath"]

    def __getitem__(self, item):
        return self._storage[item]

    def close(self):
        self._storage.close()