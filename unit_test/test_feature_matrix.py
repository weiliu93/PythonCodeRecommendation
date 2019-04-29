import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from pcr.common.feature_matrix import FeatureMatrix
from pcr.common.feature_vector import FeatureVector


def test_matrix_multiply_vector():
    matrix = FeatureMatrix(3, 3)
    matrix[0][1] = 10
    matrix[0][2] = 5
    matrix[1][0] = 3
    matrix[1][2] = 6
    matrix[2][0] = 7
    matrix[2][1] = 4

    vector = FeatureVector(3)
    vector[1] = 3
    vector[0] = 2
    vector[2] = 6

    result_vector = matrix.multiply_vector(vector)
    assert len(result_vector) == 3
    assert result_vector[0] == 60
    assert result_vector[1] == 42
    assert result_vector[2] == 26

def test_set_and_get():
    matrix = FeatureMatrix(3, 3)
    matrix_array = [
        [1, 0, 4],
        [10, 3, 6],
        [7, 9, 3]
    ]
    for i in range(3):
        for j in range(3):
            matrix[i][j] = matrix_array[i][j]

    for i in range(3):
        for j in range(3):
            assert matrix[i][j] == matrix_array[i][j]

    matrix[0][0] = 5
    assert matrix[0][0] == 5
    matrix[0][0] = 1
    assert matrix[0][0] == 1

    matrix[1][2] = 10
    assert matrix[1][2] == 10