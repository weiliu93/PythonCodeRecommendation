def byte_array_to_integer(byte_array):
    """convert byte_array into integer"""
    integer_result = 0
    for b in byte_array:
        integer_result = (integer_result << 8) + int(b)
    return integer_result


def integer_to_byte_array(integer, n):
    byte_array = bytearray()
    for index in range(n * 8 - 1, 0, -8):
        start_index, end_index, value = index, index - 7, 0
        while start_index >= end_index:
            if integer & (1 << start_index):
                value = value | (1 << (start_index - end_index))
            start_index -= 1
        byte_array.append(value)
    return byte_array
