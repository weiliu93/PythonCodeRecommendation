from pcr.computational_graph.task import Task
from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.parsing.core import Parser
from pcr.computational_graph.feature_extraction import FeatureExtraction

from pcr.logger.log_util import logger

class ParsingTask(Task):

    def _execute(self, data_bundle, from_node):
        """
        parse source code, output source code and feature set
        """
        source_code = data_bundle["code"]
        filepath = data_bundle["filepath"]
        try:
            root = Parser.spt_parse(source_code)
            features = FeatureExtraction.extract(root)
            emit_data_bundle = DataBundle(data_dict=
                                          {"code": source_code,
                                           "features": features,
                                           "filepath": filepath})
            self._emit(emit_data_bundle)
            logger.info("parsing code succeeded, filepath: {}".format(filepath))
        except Exception as e:
            # if parsing failed, ignore it
            logger.warn("parsing code pieces: {} failed".format(filepath))
            raise e