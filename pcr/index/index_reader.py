from pcr.storage.append_only_array_storage import AppendOnlyArrayStorage


class IndexReader(object):

    def __init__(self, storage_filepath):
        self._storage = AppendOnlyArrayStorage(storage_filepath)

    def __iter__(self):
        for dict_item in self._storage:
            if isinstance(dict_item, dict):
                yield dict_item["features"], dict_item["line_number"], dict_item["next_line"]

    def close(self):
        self._storage.close()