from pcr.computational_graph.task import Task
from pcr.computational_graph.parsing.core import Parser
from pcr.computational_graph.feature_extraction.core import FeatureExtraction
from pcr.computational_graph.data_bundle import DataBundle


from pcr.logger.log_util import logger


class ExtractMappingTask(Task):

    def _execute(self, data_bundle, from_node):
        code = data_bundle["code"]
        lines = code.split("\n")
        if len(lines) > 1:
            try:
                root = Parser.spt_parse("\n".join(lines[ : - 1]))
                features = FeatureExtraction.extract(root)
                self._emit(DataBundle(data_dict=
                                      {"features": features,
                                       "line_number": len(lines) - 1,
                                       "next_line": lines[- 1]}))
                logger.info("extract mapping succeeded, next line is: " + lines[- 1])
            except:
                logger.warn("extract mapping failed")
