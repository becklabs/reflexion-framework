import re


def rust_extract_tests(test_str: str):
    matches = re.findall(r"((assert_eq!|assert!)\(.*?\)[^;]*;)", test_str)
    return [match[0] for match in matches]


def python_extract_tests(input_string):
    matches = re.findall(r"assert .*?$", input_string, re.MULTILINE)
    return matches


def string_to_tests(input_string):
    input_string = input_string.strip().strip("\n")
    tests = [line for line in input_string.split("\n") if line]
    return tests
