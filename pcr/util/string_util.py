def left_padding_strings(lines):
    min_leading_spaces = 0
    for line in lines:
        min_leading_spaces = min(min_leading_spaces, get_left_padding_spaces(line))
    return [line[min_leading_spaces:] for line in lines]


def get_left_padding_spaces(line):
    index = 0
    while index < len(line) and line[index] == " ":
        index += 1
    return index
