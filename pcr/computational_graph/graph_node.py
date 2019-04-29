class GraphNode(object):
    def __init__(self, name=None):
        self._in_edges = set()
        self._out_edges = set()
        self._name = name if name else ("node-" + str(id(self)))

    @property
    def in_edges(self):
        return self._in_edges

    @property
    def out_edges(self):
        return self._out_edges

    @property
    def name(self):
        return self._name

    def add_in_edge(self, graph_edge):
        self._in_edges.add(graph_edge)

    def add_out_edge(self, graph_edge):
        self._out_edges.add(graph_edge)

    def __str__(self):
        return "(name: {}, in degree: {}, out degree: {})".format(
            self._name, len(self._in_edges), len(self._out_edges)
        )
