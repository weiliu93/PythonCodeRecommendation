from pcr.computational_graph.source_task import SourceTask
from pcr.computational_graph.data_bundle import DataBundle

from pcr.logger.log_util import logger
from pcr.util import string_util


class InputTask(SourceTask):

    def _execute(self, data_bundle):
        # preprocessing input code string first
        code = "\n".join(string_util.left_padding_strings(data_bundle["code"].split("\n")))
        # filepath is not mandatory
        filepath = data_bundle.data_dict.get("filepath", "N/A")
        try:
            self._emit(DataBundle(data_dict={"code": code, "filepath": filepath}))
            logger.debug("parse input {} succeeded".format(code))
        except:
            logger.error("parse input {} failed".format(code))
