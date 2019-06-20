from pcr.computational_graph.feature_extraction.core import FeatureExtraction
from pcr.computational_graph.task import Task
from pcr.computational_graph.parsing import Parser
from pcr.computational_graph.data_bundle import DataBundle
import multiprocessing


class Prune(Task):
    def _execute(self, data_bundle, from_node):
        query = Parser.spt_parse(data_bundle['code'])
        F1 = FeatureExtraction.extract(query)
        result_list = []
        for rankerElement in data_bundle['rank_list']:
            rankerElement.F1 = F1
            pruned_sim, pruned_tree = self._worker(rankerElement)
            rankerElement.pruned_tree = pruned_tree
            # from anytree.exporter import DotExporter
            # DotExporter(pruned_tree).to_picture("./{}.png".format(int(pruned_sim * 1000)))
            rankerElement.similarity = pruned_sim
        # with multiprocessing.Pool() as pool:
        #     result_list = pool.map(self._worker, data_bundle['rank_list'])
        # for idx, rankerElement in enumerate(data_bundle['rank_list']):
        #     rankerElement.pruned_tree = result_list[idx][1]
        #     rankerElement.pruned_sim = result_list[idx][0]
        data_bundle['rank_list'].sort(key = lambda e: e.similarity, reverse=True)
        self._emit(data_bundle)

    def _worker(self, RankerElement):
        candidate_tree = RankerElement.root
        F1 = RankerElement.F1
        # from anytree.exporter import DotExporter
        # DotExporter(candidate_tree).to_picture("./candidate_tree.png")
        candidate_tokens = list(filter(lambda leaf: leaf.is_token, candidate_tree.leaves))
        settled_pruned_tree = None
        settled_subtree = (None, None)
        max_sim = -1
        while candidate_tokens:
            reserved_tkn_idx = -1
            for idx, token in enumerate(candidate_tokens):
                connector, generated_tree = self._grow(settled_pruned_tree, token)
                pruned_tree = self._attach(settled_pruned_tree, connector, generated_tree, simple=True)
                # DotExporter(pruned_tree).to_picture("./pt_tmp.png")
                F2 = FeatureExtraction.extract(pruned_tree)
                sim = self._cal_sim(F1, F2)
                self._detach(generated_tree)
                if sim > max_sim:
                    settled_subtree = (connector, generated_tree)
                    reserved_tkn_idx = idx
                    max_sim = sim
            settled_pruned_tree = self._attach(settled_pruned_tree, settled_subtree[0], settled_subtree[1])
            # from anytree.exporter import DotExporter
            # DotExporter(settled_pruned_tree).to_picture("./big_tree.png")
            candidate_tokens.pop(reserved_tkn_idx)
        return max_sim, settled_pruned_tree


    def _roll_up(self, target_node, dup_node):
        target_node = target_node.parent
        new_node = target_node.copy()
        new_node.set_children([dup_node])
        new_node.roster = dup_node.roster
        return new_node

    def _grow(self, big_tree, seed):
        # if big_tree:
        #     from anytree.exporter import DotExporter
        #     DotExporter(big_tree).to_picture("./big_tree.png")
        generated_tree = seed.copy()
        generated_tree.roster = {}
        generated_tree.roster[generated_tree.copy_from] = generated_tree
        growing_node = seed
        while growing_node.parent:
            par_id = id(growing_node.parent)
            # from anytree.exporter import DotExporter
            # DotExporter(generated_tree).to_picture("./small_tree.png")
            if big_tree and par_id in big_tree.roster:
                return big_tree.roster[par_id], generated_tree
            generated_tree = self._roll_up(growing_node, generated_tree)
            generated_tree.roster[generated_tree.copy_from] = generated_tree
            growing_node = growing_node.parent
        return None, generated_tree

    def _detach(self, subtree):
        if not subtree.parent:
            return
        detach_from_node = subtree.parent
        new_children = detach_from_node.children[:subtree.rank - 1] + detach_from_node.children[subtree.rank:]
        detach_from_node.set_children(new_children)

    def _redirect_roster(self, tree, target_roster):
        stack = [tree]
        while stack:
            cur_node = stack.pop()
            cur_node.roster = target_roster
            for child in cur_node.children:
                stack.append(child)

    def _attach(self, left_tree, connector, right_tree, simple=False):
        if connector is None:
            return right_tree
        if right_tree.copy_from in left_tree.roster:
            return left_tree
        connector.set_children(connector.children + (right_tree,))
        if simple:
            return left_tree
        left_tree.roster.update(right_tree.roster)
        self._redirect_roster(right_tree, left_tree.roster)
        return left_tree

    def _cal_sim(self, F1, F2):
        return len(F1.intersection(F2)) / len(F1)