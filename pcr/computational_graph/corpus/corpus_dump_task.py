from pcr.computational_graph.task import Task
from pcr.corpus.corpus_writer import CorpusWriter

import os


class CorpusDumpTask(Task):

    def __init__(self, name=None, stop_timeout_window=2, corpus_path=None):
        super().__init__(name, stop_timeout_window)
        self._corpus_writer = CorpusWriter(corpus_path or os.path.join(os.curdir, "corpus_storage"))

    def _execute(self, data_bundle, from_node):
        """
        It is a termination task, don't need to emit anything
        """
        code, features, filepath = data_bundle["code"], data_bundle["features"], data_bundle["filepath"]
        self._corpus_writer.write_corpus(code, features, filepath)

    def _stop(self):
        self._corpus_writer.close()
