# pcr/computational_graph/test.py
import sys
from computational_graph.parsing.core import simple_example
from computational_graph.parsing import Parser
from computational_graph.feature_extraction import FeatureExtraction
from computational_graph.prune_reranking import Prune
import anytree
from anytree.exporter import DotExporter

# sys.path.insert(0, '/Users/shenh/work/PythonCodeRecommendation')
candidate = '''
a = {
    "b": 2,
    "cc": 234242,
    fun(): func2(),
    a: [1,2,3,4,5,6]
}
'''

query = '''
b = {
    "cc": 2,
}
'''

candidate = Parser.spt_parse(candidate)
DotExporter(candidate).to_picture("./candidate_tree.png")
candidate_features = FeatureExtraction.extract(candidate)

query = Parser.spt_parse(query)
DotExporter(query).to_picture("./query.png")
query_features = FeatureExtraction.extract(query)

data_bundle = {
    'candidate_tree': candidate,
    'query_features': query_features,
}

pp = Prune()
pt = pp._execute(data_bundle, None)
DotExporter(pt).to_picture("./pruned_tree.png")

cc = 0
# simple_example()
