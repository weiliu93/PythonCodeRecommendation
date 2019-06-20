from pcr.computational_graph.task import Task


class PrintRecommendCodeToConsoleTask(Task):

    def _execute(self, data_bundle, from_node):
        rank_list = data_bundle["rank_list"]
        with open("result.py", "w") as f:
            for rank_element in rank_list:
                f.write(str(rank_element))
                f.write("#######################################\n")
                # print(rank_element.corpus_code)
                # print("#######################################")