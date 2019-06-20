import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.preprocessing.app_set_preprocessing_task import AppSetPreprocessingTask
from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.index.extract_mapping_task import ExtractMappingTask
from pcr.computational_graph.index.index_dump_task import IndexDumpTask
from pcr.computational_graph.linear_scheduler import LinearScheduler


import os
import fire


class UpdateIndex(object):

    def update_index_from_default_dir(self):

        work_dir = os.path.join(os.path.dirname(__file__), os.path.pardir, "index_dir")
        graph = ComputationalGraph()

        app_set_task = AppSetPreprocessingTask(init_data_bundle=DataBundle(data_dict={"work_dir": work_dir}))
        extract_mapping_task = ExtractMappingTask()
        index_dump_task = IndexDumpTask()

        graph.add_edge(app_set_task, extract_mapping_task)
        graph.add_edge(extract_mapping_task, index_dump_task)

        scheduler = LinearScheduler(graph)
        scheduler.schedule()


if __name__ == "__main__":
    fire.Fire(UpdateIndex)