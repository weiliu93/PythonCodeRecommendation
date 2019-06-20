from pcr.computational_graph.task import Task


class PrintRecommendCodeToConsoleTask(Task):

    def _execute(self, data_bundle, from_node):
        rank_list = data_bundle["rank_list"]
        for rank_element in rank_list:
            print(rank_element.corpus_code)
            print("#######################################")