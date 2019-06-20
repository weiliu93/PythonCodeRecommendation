from pcr.computational_graph.source_task import SourceTask
from pcr.computational_graph.data_bundle import DataBundle

from pcr.logger.log_util import logger


class InputTask(SourceTask):

    def _execute(self, data_bundle):
        code = data_bundle["code"]
        try:
            self._emit(DataBundle(data_dict={"code": code}))
            logger.debug("parse input {} succeeded".format(code))
        except:
            logger.error("parse input {} failed".format(code))
