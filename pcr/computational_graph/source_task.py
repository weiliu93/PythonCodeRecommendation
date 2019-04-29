from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.graph_node import GraphNode


class SourceTask(object):
    def __init__(self, init_data_bundle, name=None):
        self._graph_node = GraphNode(name)
        self._init_data_bundle = init_data_bundle
        assert isinstance(init_data_bundle, DataBundle)

    @property
    def graph_node(self):
        return self._graph_node

    @property
    def name(self):
        return self._graph_node.name

    def __str__(self):
        return "graph_node: {}".format(str(self._graph_node))

    def execute(self):
        self._execute(self._init_data_bundle)
        # source task won't have more input data
        # so we can stop the entire pipeline
        self._emit(DataBundle.stop_signal())

    def _execute(self, data_bundle):
        """implement execution logic in derived class"""
        pass

    def _emit(self, data_bundle):
        assert isinstance(data_bundle, DataBundle)
        for out_edge in self._graph_node.out_edges:
            out_edge.emit(data_bundle)
