from pcr.computational_graph.query.query_task import QueryTask
from pcr.computational_graph.ranking.coarse_ranker import CoarseRanker
from pcr.computational_graph.computational_graph import ComputationalGraph
from pcr.computational_graph.linear_scheduler import LinearScheduler
from pcr.computational_graph.data_bundle import DataBundle


graph = ComputationalGraph()

code = """if a == 10:
    print('hello')"""

query_task = QueryTask(init_data_bundle=DataBundle(data_dict={"code": code}))
rank_task = CoarseRanker()

graph.add_edge(query_task, rank_task)

scheduler = LinearScheduler(graph)
scheduler.schedule()
