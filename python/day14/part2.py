from typing import List

def cycle(platform):
    # north tilt
    for row in range(1, len(platform)):
        for col in range(len(platform[0])):
            if platform[row][col] == "O":
                for rock_row in range(row - 1, -1, -1):
                    if platform[rock_row][col] in ["O", "#"]:
                        break
                    platform[rock_row][col], platform[rock_row + 1][col] = (
                        platform[rock_row + 1][col],
                        platform[rock_row][col],
                    )

    # west tilt
    for col in range(1, len(platform[0])):
        for row in range(len(platform)):
            if platform[row][col] == "O":
                for rock_col in range(col - 1, -1, -1):
                    if platform[row][rock_col] in ["O", "#"]:
                        break
                    platform[row][rock_col], platform[row][rock_col + 1] = (
                        platform[row][rock_col + 1],
                        platform[row][rock_col],
                    )

    # south tilt
    for row in range(len(platform) - 2, -1, -1):
        for col in range(len(platform[0])):
            if platform[row][col] == "O":
                for rock_row in range(row + 1, len(platform)):
                    if platform[rock_row][col] in ["O", "#"]:
                        break
                    platform[rock_row][col], platform[rock_row - 1][col] = (
                        platform[rock_row - 1][col],
                        platform[rock_row][col],
                    )

    # east tilt
    for col in range(len(platform[0]) - 2, -1, -1):
        for row in range(len(platform)):
            if platform[row][col] == "O":
                for rock_col in range(col + 1, len(platform[0])):
                    if platform[row][rock_col] in ["O", "#"]:
                        break
                    platform[row][rock_col], platform[row][rock_col - 1] = (
                        platform[row][rock_col - 1],
                        platform[row][rock_col],
                    )


def hash(platform: List[List[str]]) -> int:
    hash: int = 0
    for row, line in enumerate(platform):
        for col, item in enumerate(line):
            if item == "O":
                hash |= 1 << (row + col * len(platform[0]))
    return hash


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    platform = []
    for line in data:
        platform.append([char for char in line])

    goal = 1000000000
    seen = {}
    for index in range(goal):
        key = hash(platform)
        if key in seen:
            break
        seen[key] = index
        cycle(platform)

    prefix = seen[key]
    rock_cycle = index - prefix
    times = (goal - prefix) // rock_cycle
    actual_cycle = (goal - prefix) % rock_cycle

    for _ in range(actual_cycle):
        cycle(platform)

    total_load = 0
    for row in range(len(platform)):
        for col in range(len(platform[0])):
            if platform[row][col] == "O":
                total_load += len(platform) - row

    return total_load


if __name__ == "__main__":
    print(solution("./example.txt"))  # 64
    print(solution("./input.txt"))  # 95254
