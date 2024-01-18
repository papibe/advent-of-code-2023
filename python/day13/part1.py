from typing import List


def get_vertical_reflection(pattern: List[str]) -> int:
    for col in range(len(pattern[0]) - 1):
        left: int = col
        right: int = col + 1
        while left >= 0 and right < len(pattern[0]):
            for row in range(len(pattern)):
                if pattern[row][left] != pattern[row][right]:
                    break
            else:
                left -= 1
                right += 1
                continue
            break
        else:
            return col + 1
    return 0


def get_horizontal_reflection(pattern: List[str]) -> int:
    for row in range(len(pattern) - 1):
        up: int = row
        down: int = row + 1
        while up >= 0 and down < len(pattern):
            for col in range(len(pattern[0])):
                if pattern[up][col] != pattern[down][col]:
                    break
            else:
                up -= 1
                down += 1
                continue
            break
        else:
            return row + 1
    return 0


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        patterns: List[str] = fp.read().split("\n\n")

    total_sum: int = 0
    for raw_pattern in patterns:
        pattern: List[str] = raw_pattern.splitlines()

        # check vertical reflection
        col = get_vertical_reflection(pattern)
        total_sum += col

        # check horizontal reflection
        row = get_horizontal_reflection(pattern)
        total_sum += row * 100

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 405
    print(solution("./input.txt"))  # 33122
