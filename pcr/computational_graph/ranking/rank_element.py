from pcr.computational_graph.parsing.core import Parser


class RankElement(object):
    def __init__(self, similarity, corpus_code, corpus_filepath):
        self._similarity = similarity
        self._corpus_code = corpus_code
        self._corpus_filepath = corpus_filepath
        self._corpus_code_line_number = len(self._corpus_code.split("\n"))
        self._root = Parser.spt_parse(self._corpus_code)

    @property
    def root(self):
        return self._root

    @property
    def corpus_code_line_number(self):
        return self._corpus_code_line_number

    @property
    def similarity(self):
        return self._similarity
    
    @similarity.setter
    def similarity(self, value):
        self._similarity = value

    @property
    def corpus_code(self):
        return self._corpus_code

    @property
    def corpus_filepath(self):
        return self._corpus_filepath

    def __str__(self):
        return "{}\n{}\n{}\n".format(self.similarity, self.corpus_code, self.corpus_filepath)