def left_padding_strings(lines):
    min_leading_spaces = 1000000000
    for line in lines:
        line = line.replace("\t", "    ")
        if not is_empty_string(line):
            min_leading_spaces = min(min_leading_spaces, get_left_padding_spaces(line))
    return [line[min_leading_spaces:] for line in lines if not is_empty_string(line)]


def get_left_padding_spaces(line):
    index = 0
    while index < len(line) and line[index] == " ":
        index += 1
    return index


def is_empty_string(line):
    return line.strip() == ""