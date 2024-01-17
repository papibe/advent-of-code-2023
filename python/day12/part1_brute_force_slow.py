from typing import List


def count(spring: List[str]) -> List[int]:

    counter: int = 0
    result: List[int] = []
    index: int = 0
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


def equal(s: List[int], t: List[int]) -> bool:
    if len(s) != len(t):
        return False
    for i in range(len(s)):
        if s[i] != t[i]:
            return False
    return True


def check(spring: str, numbers: List[int]) -> int:
    def _check(index: int, possible: List[str]) -> int:
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
        data: List[str] = fp.read().splitlines()

    total_sum: int = 0
    for line in data:
        springs, numbers_str = line.split(" ")
        numbers: List[int] = [int(n) for n in numbers_str.split(",")]

        total_sum += check(springs, numbers)

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 21
    # print(solution("./input.txt"))  # 7490
