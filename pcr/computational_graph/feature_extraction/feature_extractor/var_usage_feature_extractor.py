from .util import FeatureExtractor


class VarUsageFeatureExtractor(FeatureExtractor):
    def __init__(self):
        super(VarUsageFeatureExtractor, self).__init__()
        self._leaves = []
        self._idx = -1

    def setup(self, root, **kwargs):
        self._leaves = root.leaves
    
    def register_action(self, node):
        if node.is_token:
            self._idx += 1
            predecessor_idx = self._search_usage(range(self._idx, -1, -1), node.label)
            predecessor_ctx = self._get_context(predecessor_idx)
            successor_idx = self._search_usage(range(self._idx, len(self._leaves), 1), node.label)
            successor_ctx = self._get_context(successor_idx)
            if any([successor_ctx is None, predecessor_ctx is None]):
                return
            self._buffer.append((predecessor_ctx, successor_ctx))

    def _get_context(self, leaf_idx):
        if leaf_idx < 0 or leaf_idx >= len(self._leaves):
            return None
        leaf = self._leaves[leaf_idx]
        return (leaf.rank, leaf.parent.label)

    def _search_usage(self, search_range, label):
        for i in search_range:
            if self._leaves[i].label == label:
                return i
        return None