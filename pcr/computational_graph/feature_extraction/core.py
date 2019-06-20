import ast
from .feature_extractor.parent_feature_extractor import ParentFeatureExtractor
from .feature_extractor.token_feature_extractor import TokenFeatureExtractor
from .feature_extractor.var_usage_feature_extractor import VarUsageFeatureExtractor
import itertools

__all__ = ["FeatureExtraction"]


class FeatureExtraction(object):
    @staticmethod
    def extract(tree):
        '''Extract the features.
        Args:
            tree (..parsing.core.SptNode): The Simplified Parsed Tree root.
        Return:
            features (set): The set containing all features in the tree.
        '''
        visitor = _TreeVisitor(tree)
        visitor.visit(tree)
        return visitor.collect_features()


class _TreeVisitor(ast.NodeVisitor):
    '''This visitor is not meant to only visit AST node,
    but also any self-defined nodes.
    '''
    def __init__(self, root):
        super(_TreeVisitor, self).__init__()
        self._feature_pool = set()
        self._feature_extractors = [
            ParentFeatureExtractor(),
            TokenFeatureExtractor(),
            VarUsageFeatureExtractor(),
            ]
        for extor in self._feature_extractors:
            extor.setup(root)

    def _register_action(self, node):
        for ft_extractor in self._feature_extractors:
            ft_extractor.register_action(node)

    def visit_SptNode(self, node):
        self._register_action(node)
        for child in node.children:
            self.visit(child)
    
    def visit_TokenNode(self, node):
        self._register_action(node)

    def collect_features(self):
        for feature in itertools.chain(*self._feature_extractors):
            self._feature_pool.add(feature)
        return self._feature_pool
