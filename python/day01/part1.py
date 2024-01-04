from typing import List


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    addition: int = 0
    for line in data:
        digits: List[str] = []
        for char in line:
            if char.isnumeric():
                digits.append(char)

        # adding number composed from first and last digits
        addition += int(digits[0] + digits[-1])

    return addition


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 142
    print(solution("./input.txt"))  # 54667
