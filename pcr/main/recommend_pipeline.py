import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from pcr.computational_graph.input.input_task import InputTask
from pcr.computational_graph.ranking.coarse_ranker import CoarseRanker
from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.linear_scheduler import LinearScheduler
from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.output.print_recommend_code_to_console import PrintRecommendCodeToConsoleTask


import fire


class RecommendCorpus(object):

    def recommend_code_piece(self, code):
        graph = ComputationalGraph()
        query_task = InputTask(init_data_bundle=DataBundle(data_dict={"code": code}))
        rank_task = CoarseRanker()
        print_recommend_code_to_console = PrintRecommendCodeToConsoleTask()

        graph.add_edge(query_task, rank_task)
        graph.add_edge(rank_task, print_recommend_code_to_console)

        scheduler = LinearScheduler(graph)
        scheduler.schedule()

    def recommend_based_on_previous_input(self, previous_code_lines):
        # TODO

        return previous_code_lines

    def recommend_based_on_prefix(self, prefix):
        # TODO

        return prefix

if __name__ == "__main__":
    fire.Fire(RecommendCorpus)
