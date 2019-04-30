import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from pcr.common.feature_vector import FeatureVector


def test_vector_set_and_get():
    vector = FeatureVector(10)
    vector[0] = 4
    vector[2] = 9
    vector[7] = 10
    vector[8] = 20

    assert vector[0] == 4
    assert vector[2] == 9
    assert vector[7] == 10
    assert vector[8] == 20

    for index in filter(lambda index: index not in [0, 2, 7, 8], range(10)):
        assert vector[index] == 0

    vector[7] = 0
    assert vector[7] == 0

    try:
        vector[10] = 10
        assert False, "index out of bound"
    except:
        pass

    try:
        vector[-1] = 10
        assert False, "index could not be negative"
    except:
        pass

    try:
        vector["hello"] = 10
        assert False, "index should be integer"
    except:
        pass


def test_vector_one_hot():
    vector = FeatureVector(10)
    vector[0] = 10
    vector[2] = 100
    vector[3] = 7
    vector[7] = 10
    vector[9] = 1
    one_hot_vector = vector.one_hot_vector()
    index_list = [0, 2, 3, 7, 9]
    for index in range(10):
        if index in index_list:
            assert one_hot_vector[index] == 1
        else:
            assert one_hot_vector[index] == 0


def test_vector_dot_product():
    vector1 = FeatureVector(10)
    vector2 = FeatureVector(10)

    vector1[0] = 5
    vector1[4] = 8
    vector1[8] = 9

    vector2[0] = 2
    vector2[3] = 6
    vector2[5] = 4
    vector2[8] = 3

    result = vector1.dot_product(vector2)
    assert result == 37


def test_vector_sum():
    vector = FeatureVector(10)
    vector[0] = 10
    vector[3] = 5
    vector[9] = 9
    assert vector.sum() == 24


def test_vector_intersect():
    vector1, vector2 = FeatureVector(10), FeatureVector(10)
    vector1[0] = 10
    vector1[4] = 2
    vector1[7] = 8

    vector2[0] = 4
    vector2[3] = 7
    vector2[7] = 12

    vector = vector1.intersect(vector2)
    # 0:4, 7: 12
    assert vector[0] == 4
    assert vector[7] == 8
    for index in filter(lambda index: index not in [0, 7], range(10)):
        assert vector[index] == 0


def test_vector_add():
    vector1, vector2 = FeatureVector(5), FeatureVector(5)
    vector1[0] = 10
    vector1[2] = 5
    vector1[4] = 7
    vector2[1] = 4
    vector2[4] = 8
    vector = vector1.add(vector2)
    assert vector[0] == 10
    assert vector[1] == 4
    assert vector[2] == 5
    assert vector[3] == 0
    assert vector[4] == 15
    assert vector.sum() == 34


def test_vector_intersect_with_different_length():
    vector1, vector2 = FeatureVector(10), FeatureVector(14)
    try:
        vector1.intersect(vector2)
        assert (
            False
        ), "Vector intersection between two vectors with different length is illegal"
    except:
        pass
