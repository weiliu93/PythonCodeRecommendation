import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from pcr.util.bytes_util import byte_array_to_integer
from pcr.util.bytes_util import integer_to_byte_array


def test_byte_array_to_integer():
    byte_array = bytearray()
    byte_array.append(1)
    byte_array.append(2)
    byte_array.append(3)
    assert byte_array_to_integer(byte_array) == (1 << 16) + (2 << 8) + 3


def test_integer_to_byte_array():
    byte_array = integer_to_byte_array(300, 3)
    assert len(byte_array) == 3
    assert byte_array[0] == 0
    assert byte_array[1] == 1
    assert byte_array[2] == 44