from pcr.common.feature_vector import FeatureVector


class FeatureMatrix(object):

    def __init__(self, n, m):
        assert isinstance(n, int) and isinstance(m, int)
        assert n > 0 and m > 0

        self._vector_rows = []
        self.n, self.m = n, m
        for _ in range(n):
            self._vector_rows.append(FeatureVector(m))

    def __setitem__(self, key, value):
        assert isinstance(key, int)
        assert key >= 0 and key < self.n
        assert isinstance(value, FeatureVector)
        assert value.length == self.m
        self._vector_rows[key] = value

    def __getitem__(self, item):
        assert isinstance(item, int)
        assert item >= 0 and item < self.n
        return self._vector_rows[item]

    def multiply_vector(self, another_vector):
        assert isinstance(another_vector, FeatureVector)
        assert another_vector.length == self.m
        result_vector = FeatureVector(self.n)
        for index, vector in enumerate(self._vector_rows):
            result = vector.dot_product(another_vector)
            if result != 0:
                result_vector[index] = result
        return result_vector

    def __str__(self):
        result_list = []
        for vector in self._vector_rows:
            result_list.append(str(vector))
        return "(" + ", ".join(result_list) + ")"

    def __len__(self):
        return self.n * self.m