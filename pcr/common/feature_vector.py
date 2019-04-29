class FeatureVector(object):

    def __init__(self, length):
        assert isinstance(length, int)
        assert length > 0
        self._length = length
        self._value_dict = {}

    @property
    def length(self):
        return self._length

    def __iter__(self):
        for key, value in self._value_dict.items():
            yield key, value

    def __len__(self):
        return self._length

    def __setitem__(self, key, value):
        assert isinstance(key, int) and isinstance(value, int)
        assert key >= 0 and key < self._length
        self._value_dict[key] = value

    def __getitem__(self, item):
        assert isinstance(item, int)
        assert item >= 0 and item < self._length
        return self._value_dict.get(item, 0)

    def __str__(self):
        result_list = []
        for key, value in self:
            result_list.append((key, value))
        result_list.sort()
        return "(" + ", ".join(map(lambda tuple: "{}: {}".format(tuple[0], tuple[1]), result_list)) + ")"

    def one_hot_vector(self):
        """convert current vector into one-hot vector"""
        result_vector = FeatureVector(self._length)
        for key, value in filter(lambda tuple: tuple[1] != 0, self):
            result_vector[key] = 1
        return result_vector

    def dot_product(self, another_vector):
        """vector dot product"""
        assert isinstance(another_vector, FeatureVector)
        assert self.length == another_vector.length
        current_vector, result_vector = self, FeatureVector(self.length)
        if current_vector.length > another_vector.length:
            current_vector, another_vector = another_vector, current_vector
        result = 0
        for key, value in current_vector:
            result += value * another_vector[key]
        return result

    def sum(self):
        result = 0
        for key, value in self._value_dict.items():
            result += value
        return result

    def intersect(self, another_vector):
        assert isinstance(another_vector, FeatureVector)
        assert self.length == another_vector.length
        intersection_vector = FeatureVector(self.length)
        for key, value in self:
            intersection_value = min(value, another_vector[key])
            if intersection_value != 0:
                intersection_vector[key] = intersection_value
        return intersection_vector

    def feature_vector_similarity(self, another_vector):
        s = self.sum()
        assert s != 0, "Similarity doesn't work in empty vector"
        intersection = self.intersect(another_vector)
        return intersection.sum() / s
