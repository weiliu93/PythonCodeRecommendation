from pcr.computational_graph.task import Task
from pcr.corpus.corpus_reader import CorpusReader
from pcr.computational_graph.feature_extraction.core import FeatureExtraction
from pcr.computational_graph.parsing.core import Parser
from pcr.computational_graph.data_bundle import DataBundle
from .rank_element import RankElement

import os


class CoarseRanker(Task):

    def __init__(self, name=None, stop_timeout_window=0.1, corpus_path=None, rank_threshold=100):
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
            similarity = len(corpus_features & query_features)
            result_list.append(RankElement(similarity, corpus_code, filepath))
        result_list.sort(key = lambda e: (e.similarity, - abs(e.corpus_code_line_number - code_lines)), reverse=True)
        emit_data_bundle = DataBundle(data_dict=
                                 {"code": query_code,
                                  "rank_list": result_list[: self._rank_threshold]})
        self._emit(emit_data_bundle)