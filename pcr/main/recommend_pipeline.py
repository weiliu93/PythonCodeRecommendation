import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from pcr.computational_graph.input.input_task import InputTask
from pcr.computational_graph.ranking.coarse_ranker import CoarseRanker
from pcr.computational_graph.ranking.fine_ranker import Prune
from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.linear_scheduler import LinearScheduler
from pcr.computational_graph.data_bundle import DataBundle
from pcr.computational_graph.output.print_recommend_code_to_console import PrintRecommendCodeToConsoleTask
from pcr.computational_graph.ranking.index_ranker import IndexRanker


import fire


class RecommendCorpus(object):

    def recommend_code_piece(self, code):
        graph = ComputationalGraph()
        query_task = InputTask(init_data_bundle=DataBundle(data_dict={"code": code}))
        rank_task = CoarseRanker()
        prune_task = Prune()
        print_recommend_code_to_console = PrintRecommendCodeToConsoleTask()

        graph.add_edge(query_task, rank_task)
        # graph.add_edge(rank_task, prune_task)
        # graph.add_edge(prune_task, print_recommend_code_to_console)
        graph.add_edge(rank_task, print_recommend_code_to_console)

        scheduler = LinearScheduler(graph)
        scheduler.schedule()

    def recommend_based_on_previous_input(self, previous_code):
        graph = ComputationalGraph()

        query_task = InputTask(init_data_bundle=DataBundle(data_dict={"code": previous_code}))
        index_ranker = IndexRanker()
        graph.add_edge(query_task, index_ranker)

        scheduler = LinearScheduler(graph)
        scheduler.schedule()

    def recommend_based_on_prefix(self, prefix):
        # TODO

        return prefix

if __name__ == "__main__":
    # fire.Fire(RecommendCorpus)
    rec = RecommendCorpus()
#     code = '''
# f = open(a, "w")
# '''
    code = '''
class fdsafdsaf(streamingcommand):
    pass
'''
    rec.recommend_code_piece(code)
