import queue
import copy

from pcr.computational_graph.data_bundle import DataBundle
from pcr.logger.log_util import logger


class GraphEdge(object):
    """Lock was used in BlockingQueue, graph edge couldn't be pickle. This class can not support multiprocessing"""

    def __init__(self, from_node, to_node):
        self._queue = queue.Queue()
        # store from_node and to_node
        self._from_node = from_node
        self._to_node = to_node

    @property
    def from_node(self):
        return self._from_node

    @property
    def to_node(self):
        return self._to_node

    def __str__(self):
        return "(from: {}, to: {})".format(self._from_node, self._to_node)

    def __hash__(self):
        return hash(self._from_node) * 31 + hash(self._to_node)

    def __eq__(self, other):
        assert isinstance(other, GraphEdge)
        return self.from_node == other.from_node and self.to_node == other.to_node

    def emit(self, data_bundle):
        assert isinstance(data_bundle, DataBundle)
        self._queue.put((copy.copy(data_bundle), self._from_node), block=True)
        logger.debug(
            "emit data in edge",
            from_node=self.from_node,
            to_node=self.to_node,
            data_bundle=data_bundle,
        )

    def pull(self, blocked=False, timeout=None):
        try:
            data = self._queue.get(block=blocked, timeout=timeout)
            logger.debug(
                "pull data in edge succeeded",
                from_node=self._from_node,
                to_node=self._to_node,
                data=data,
            )
            return data
        except:
            # no data available
            logger.debug(
                "pull data in edge failed",
                from_node=self._from_node,
                to_node=self._to_node,
            )
            return (None, None)
