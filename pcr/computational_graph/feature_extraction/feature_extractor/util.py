class FeatureExtractor(object):
    DRILL = 'drill' # Denotes the action of visiting one's child.
    HOP = 'hop' # Denotes the action of just finishing a subtree's traversal and starting traversal of another subtree.
    KEYWORDS = []

    def __init__(self):
        self._buffer = []

    def register_action(self, node):
        raise NotImplementedError

    def setup(self, root, **kwargs):
        return

    def yield_feature(self):
        while self._buffer:
            feature = self._buffer.pop()
            yield feature

    def __iter__(self):
        while self._buffer:
            feature = self._buffer.pop()
            yield feature

    def __next__(self):
        if not self._buffer:
            raise StopIteration
        return self._buffer.pop()