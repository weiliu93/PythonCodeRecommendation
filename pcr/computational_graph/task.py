import time
import random

from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.graph_node import GraphNode


class Task(object):
    def __init__(self, name=None, stop_timeout_window=2):
        """
        :param name:                    customize task's name
        :param stop_timeout_window:     timeout window when stop signal received, time unit is second
        """
        self._graph_node = GraphNode(name)
        self._stop_timeout_window = stop_timeout_window

    @property
    def graph_node(self):
        return self._graph_node

    @property
    def name(self):
        return self._graph_node.name

    def __str__(self):
        return "graph_node: {}".format(str(self._graph_node))

    def execute(self):
        stop = False
        while True:
            data_list = self.__batch_pull()
            if data_list:
                for data_bundle, from_node in data_list:
                    if data_bundle.is_stop_signal():
                        stop = True
                    else:
                        # execute non-stop data bundle only
                        self._execute(data_bundle, from_node)
            else:
                # stop signal received and can not fetch data at current time
                # gracefully shutdown current task, collect possible incoming
                # tasks in timeout windows
                if stop:
                    data_list = self.__batch_pull(
                        blocked=True, timeout=self._stop_timeout_window
                    )
                    for data_bundle, from_node in data_list:
                        if not data_bundle.is_stop_signal():
                            self._execute(data_bundle, from_node)
                    break
                else:
                    # yield thread if no stop signal received
                    time.sleep(0)
        # stop following tasks
        self._emit(DataBundle.stop_signal())
        # stop task
        self._stop()

    def _execute(self, data_bundle, from_node):
        """implement execution logic in derived class"""
        pass

    def _stop(self): pass

    def _emit(self, data_bundle, task_emit_strategy=None):
        """Default emit strategy is fanout"""
        assert isinstance(data_bundle, DataBundle)
        task_emit_strategy = task_emit_strategy or FanoutStrategy
        assert issubclass(task_emit_strategy, TaskEmitStrategy)

        strategy_instance = task_emit_strategy(self.graph_node, data_bundle)
        strategy_instance.action()

    def __batch_pull(self, blocked=False, timeout=None):
        pull_result = []
        for in_edge in self._graph_node.in_edges:
            data_bundle, from_node = in_edge.pull(blocked, timeout)
            if data_bundle and from_node:
                pull_result.append((data_bundle, from_node))
        return pull_result


class TaskEmitStrategy(object):

    def __init__(self, graph_node, data_bundle):
        self._graph_node = graph_node
        self._data_bundle = data_bundle

    def action(self): pass

class FanoutStrategy(TaskEmitStrategy):

    def __init__(self, graph_node, data_bundle):
        super().__init__(graph_node, data_bundle)

    def action(self):
        for out_edge in self._graph_node.out_edges:
            out_edge.emit(self._data_bundle)

class RandomDispatchStrategy(TaskEmitStrategy):

    def __init__(self, graph_node, data_bundle):
        super().__init__(graph_node, data_bundle)

    def action(self):
        """reservoir sampling"""
        cnt, edge_chosen = 0 , None
        for out_edge in self._graph_node.out_edges:
            cnt += 1
            if random.randint(0, cnt - 1) == 0:
                edge_chosen = out_edge
        edge_chosen.emit(self._data_bundle)

class TargetDispatchStrategy(TaskEmitStrategy):

    def __init__(self, graph_node, data_bundle, target_node):
        super().__init__(graph_node, data_bundle)
        self._target_node = target_node

    def action(self):
        for out_edge in self._graph_node.out_edges:
            if out_edge.to_node == self._target_node:
                out_edge.emit(self._data_bundle)
                return