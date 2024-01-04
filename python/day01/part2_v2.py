from typing import Dict, List

DIGITS: Dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    addition: int = 0
    for line in data:
        numbers: Dict[int, int] = {}
        min_index: int = len(line)
        max_index: int = -1

        # check for spelled out digits
        for k, v in DIGITS.items():
            # check for ALL occurrences of a digit
            index: int = line.find(k)
            while index >= 0:
                max_index = max(max_index, index)
                min_index = min(min_index, index)

                numbers[index] = v
                index = line.find(k, index + len(k))

        addition += (numbers[min_index] * 10) + numbers[max_index]

    return addition


if __name__ == "__main__":
    print(solution("./example2.txt"))  # 281
    print(solution("./input.txt"))  # 54203
