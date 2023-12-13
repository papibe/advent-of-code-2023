import re
from collections import deque


def count(spring):

    counter = 0
    result = []
    index = 0
    while index < len(spring):
        while index < len(spring) and spring[index] == ".":
            index += 1
        if index >= len(spring):
            break
        counter = 0
        while index < len(spring) and spring[index] == "#":
            counter += 1
            index += 1
        result.append(counter)

    return result


def equal(s, t):
    if len(s) != len(t):
        return False
    for i in range(len(s)):
        if s[i] != t[i]:
            return False
    return True


def check(spring, numbers):
    def _check(index, possible):
        if index >= len(spring):
            if equal(count(possible), numbers):
                return 1
            else:
                return 0

        while index < len(spring) and spring[index] != "?":
            possible.append(spring[index])
            index += 1

        if index >= len(spring):
            if equal(count(possible), numbers):
                return 1
            else:
                return 0

        local_result = 0
        for char in ["#", "."]:
            possible.append(char)
            local_result += _check(index + 1, possible[:])
            possible.pop()

        return local_result

    return _check(0, [])


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    total_sum = 0
    for line in data:
        springs, numbers_str = line.split(" ")
        numbers = [int(n) for n in numbers_str.split(",")]

        res = check(springs, numbers)
        total_sum += res

    return total_sum


if __name__ == "__main__":
    # print(solution("./example.txt"))  # 21
    print(solution("./input.txt"))  # 7490
