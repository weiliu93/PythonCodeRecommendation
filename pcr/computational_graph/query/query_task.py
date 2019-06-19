from pcr.computational_graph.source_task import SourceTask
from pcr.computational_graph.data_bundle import DataBundle

from pcr.logger.log_util import logger


class QueryTask(SourceTask):

    def _execute(self, data_bundle):
        code = data_bundle["code"]
        try:
            self._emit(DataBundle(data_dict={"code": code}))
            logger.debug("parse query {} succeeded".format(code))
        except:
            logger.error("parse query {} failed".format(code))
