from pcr.computational_graph.task import Task
from pcr.corpus.corpus_reader import CorpusReader
from pcr.computational_graph.parsing.core import Parser
from pcr.computational_graph.feature_extraction.core import FeatureExtraction
from pcr.computational_graph.data_bundle import DataBundle

import os


class CoarseRanker(Task):

    def __init__(self, name=None, stop_timeout_window=2, corpus_path=None, rank_threshold=1000):
        super().__init__(name, stop_timeout_window)
        self._corpus_reader = CorpusReader(corpus_path or os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "main", "corpus_storage"))
        self._rank_threshold = rank_threshold

    def _execute(self, data_bundle, from_node):
        """
        choose top ranked code pieces based on set intersection
        """
        query_code = data_bundle["code"]
        code_lines = len(query_code.split("\n"))
        query_features = FeatureExtraction.extract(Parser.spt_parse(query_code))
        result_list = []
        for corpus_code, corpus_features, filepath in self._corpus_reader:
            result_list.append(RankElement(len(corpus_features & query_features), corpus_code, filepath))
        result_list.sort(key = lambda e: (e.intersection_size, - abs(e.corpus_code_line_number - code_lines)), reverse=True)
        emit_data_bundle = DataBundle(data_dict=
                                 {"code": query_code,
                                  "rank_list": result_list[: self._rank_threshold]})
        self._emit(emit_data_bundle)

class RankElement(object):
    def __init__(self, intersection_size, corpus_code, corpus_filepath):
        self._intersection_size = intersection_size
        self._corpus_code = corpus_code
        self._corpus_filepath = corpus_filepath
        self._corpus_code_line_number = len(self._corpus_code.split("\n"))
        self._root = Parser.spt_parse(self._corpus_code)

    @property
    def root(self):
        return self._root

    @property
    def corpus_code_line_number(self):
        return self._corpus_code_line_number

    @property
    def intersection_size(self):
        return self._intersection_size

    @property
    def corpus_code(self):
        return self._corpus_code

    @property
    def corpus_filepath(self):
        return self._corpus_filepath

    def __str__(self):
        return "{}\n{}\n{}\n".format(self.intersection_size, self.corpus_code, self.corpus_filepath)