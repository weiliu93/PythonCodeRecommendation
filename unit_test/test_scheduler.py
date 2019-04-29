import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.linear_scheduler import LinearScheduler
from pcr.computational_graph.multi_thread_scheduler import MultiThreadScheduler
from pcr.computational_graph.source_task import SourceTask
from pcr.computational_graph.task import Task
from pcr.computational_graph.data_bundle import DataBundle


def test_linear_scheduler():
    """
    tasks chain, transfer count between tasks, then update count value
    """
    result_list = []

    class Task1(SourceTask):
        def _execute(self, data_bundle):
            data_bundle["count"] += 1
            result_list.append(data_bundle["count"])
            self._emit(data_bundle)

    class Task2(Task):
        def _execute(self, data_bundle, from_node):
            data_bundle["count"] += 1
            result_list.append(data_bundle["count"])
            self._emit(data_bundle)

    prev_task = Task1(init_data_bundle=DataBundle(data_dict={"count": 0}))
    graph = ComputationalGraph()
    for _ in range(99):
        current_task = Task2(stop_timeout_window=0.1)
        graph.add_edge(prev_task, current_task)
        prev_task = current_task

    scheduler = LinearScheduler(graph)
    scheduler.schedule()

    assert result_list == list(range(1, 101, 1))


def test_multi_thread_scheduler():
    """
    tasks chain, transfer count between tasks, then update count value
    """
    result_list = []

    class Task1(SourceTask):
        def _execute(self, data_bundle):
            data_bundle["count"] += 1
            result_list.append(data_bundle["count"])
            self._emit(data_bundle)

    class Task2(Task):
        def _execute(self, data_bundle, from_node):
            data_bundle["count"] += 1
            result_list.append(data_bundle["count"])
            self._emit(data_bundle)

    prev_task = Task1(init_data_bundle=DataBundle(data_dict={"count": 0}))
    graph = ComputationalGraph()
    for _ in range(99):
        current_task = Task2(stop_timeout_window=0.1)
        graph.add_edge(prev_task, current_task)
        prev_task = current_task

    scheduler = MultiThreadScheduler(graph)
    scheduler.schedule()

    assert result_list == list(range(1, 101, 1))
