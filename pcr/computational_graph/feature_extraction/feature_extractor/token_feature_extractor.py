from .util import FeatureExtractor


class TokenFeatureExtractor(FeatureExtractor):
    DEEP = 3

    def __init__(self):
        super(TokenFeatureExtractor, self).__init__()

    def register_action(self, node):
        if node.is_token and node.label not in FeatureExtractor.KEYWORDS:
            self._buffer.append(node.label)