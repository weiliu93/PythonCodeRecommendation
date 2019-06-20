from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.task import Task
from pcr.computational_graph.source_task import SourceTask


import os

class UpdateIndex(object):

    def update_index_from_default_dir(self):

        work_dir = os.path.join(os.path.dirname(__file__), os.path.pardir, "index_dir")
        graph = ComputationalGraph()

        # feature_set -> next line