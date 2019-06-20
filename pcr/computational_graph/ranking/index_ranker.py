from pcr.computational_graph.task import Task
from pcr.computational_graph.parsing.core import Parser
from pcr.computational_graph.feature_extraction.core import FeatureExtraction
from pcr.index.index_reader import IndexReader
from pcr.logger.log_util import logger

import os

class IndexRanker(Task):

    def __init__(self, name=None, stop_timeout_window=2, index_path=None):
        super().__init__(name, stop_timeout_window)
        self._index_reader = IndexReader(index_path or os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "main", "index_storage"))

    def _execute(self, data_bundle, from_node):
        code = data_bundle["code"]
        try:
            features = FeatureExtraction.extract(Parser.spt_parse(code))
            code_line_number = len(code.split("\n"))
            max_intersection, min_line_number_diff, ans = 0, 1000000000, ""

            for index_features, line_number, next_line in self._index_reader:
                intersection = len(features & index_features)
                if intersection > max_intersection or \
                        (intersection == max_intersection and abs(code_line_number - line_number) < min_line_number_diff):
                    max_intersection = intersection
                    min_line_number_diff = abs(code_line_number - line_number)
                    ans = next_line
            print(ans)
            logger.info("index ranking succeeded, next line is: {}".format(ans))
        except:
            logger.warn("index ranking failed")