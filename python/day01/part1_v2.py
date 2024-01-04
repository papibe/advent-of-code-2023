from typing import List, Set

DIGITS: Set[str] = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    addition: int = 0
    for line in data:
        # get first digit's index
        for index in range(len(line)):
            if line[index] in DIGITS:
                min_index = index
                break
        # get last digit's index
        for index in range(len(line) - 1, -1, -1):
            if line[index] in DIGITS:
                max_index = index
                break

        # adding calibration value (composed from first and last digits)
        addition += int(line[min_index] + line[max_index])

    return addition


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 142
    print(solution("./input.txt"))  # 54667
