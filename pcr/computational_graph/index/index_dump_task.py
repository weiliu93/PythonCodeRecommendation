from pcr.computational_graph.task import Task
from pcr.index.index_writer import IndexWriter


import os


class IndexDumpTask(Task):

    def __init__(self, name=None, stop_timeout_window=0.1, index_path=None):
        super().__init__(name, stop_timeout_window)
        self._index_writer = IndexWriter(index_path or os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "main", "index_storage"))

    def _execute(self, data_bundle, from_node):
        features, line_number, next_line = data_bundle["features"], data_bundle["line_number"], data_bundle["next_line"]
        self._index_writer.write(features, line_number, next_line)