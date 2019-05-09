from .util import FeatureExtractor


class ParentFeatureExtractor(FeatureExtractor):
    DEEP = 3

    def __init__(self):
        super(ParentFeatureExtractor, self).__init__()

    def register_action(self, node):
        if node.is_token and node.label not in FeatureExtractor.KEYWORDS:
            counter = 0
            while counter < self.DEEP and node.parent:
                self._buffer.append(("#VAR", node.rank, node.parent.label))
                node = node.parent
                counter += 1
