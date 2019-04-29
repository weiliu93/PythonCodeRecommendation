from pcr.computational_graph.computational_graph import ComputationalGraph


class Scheduler(object):
    def __init__(self, computational_graph):
        assert isinstance(computational_graph, ComputationalGraph)
        self._computational_graph = computational_graph
        # force validation when initializing scheduler
        self._computational_graph.validate()

    @property
    def graph(self):
        return self._computational_graph

    def reset(self):
        self._computational_graph.reset()

    def schedule(self):
        raise NotImplementedError(
            "Please use derived scheduler class, schedule is not available here"
        )
