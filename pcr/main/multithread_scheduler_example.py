from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.source_task import SourceTask
from pcr.computational_graph.task import Task
from pcr.computational_graph.multi_thread_scheduler import MultiThreadScheduler
from pcr.computational_graph.task import RandomDispatchStrategy




class SourceTaskStub(SourceTask):
    def _execute(self, data_bundle):
        for i in range(100):
            self._emit(DataBundle(data_dict={"value": i}), RandomDispatchStrategy)

class IntermediateTask(Task):
    def __init__(self, name):
        super().__init__(name, stop_timeout_window=0.2)
    def _execute(self, data_bundle, from_node):
        self._emit(data_bundle)

class TerminationTask(Task):
    def _execute(self, data_bundle, from_node):
        print(data_bundle["value"])


# TODO fix bug in multi-thread for shen's scenario

graph = ComputationalGraph()
source = SourceTaskStub(init_data_bundle=DataBundle(data_dict={}))


tasks = []
for _ in range(2):
    tasks.append(IntermediateTask("name " + str(_)))
termination_task = TerminationTask("termination")

for i in range(2):
    graph.add_edge(source, tasks[i])
for i in range(2):
    graph.add_edge(tasks[i], termination_task)


scheduler = MultiThreadScheduler(graph)
scheduler.schedule()