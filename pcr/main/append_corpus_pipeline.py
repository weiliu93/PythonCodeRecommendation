from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.linear_scheduler import LinearScheduler

from pcr.computational_graph.preprocessing.app_set_preprocessing_task import AppSetPreprocessingTask
from pcr.computational_graph.parsing.parsing_task import ParsingTask
from pcr.computational_graph.corpus.corpus_dump_task import CorpusDumpTask

from pcr.computational_graph.data_bundle import DataBundle

import os


app_dir = os.path.abspath(os.path.join(os.path.pardir, "corpus_dir"))
graph = ComputationalGraph()

app_set_task = AppSetPreprocessingTask(init_data_bundle=DataBundle(data_dict={"corpus_dir": app_dir}))
parsing_task = ParsingTask()
corpus_dump_task = CorpusDumpTask()

graph.add_edge(app_set_task, parsing_task)
graph.add_edge(parsing_task, corpus_dump_task)

scheduler = LinearScheduler(graph)

scheduler.schedule()