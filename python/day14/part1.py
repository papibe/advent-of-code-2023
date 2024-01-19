from typing import List


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    platform: List[List[str]] = []
    for line in data:
        platform.append([char for char in line])

    # tilt
    for row in range(1, len(platform)):
        for col in range(len(platform[0])):
            item: str = platform[row][col]
            if item == "O":
                rock_row: int = row
                for rock_row in range(row - 1, -1, -1):
                    if platform[rock_row][col] in ["O", "#"]:
                        break
                    # "."
                    platform[rock_row][col], platform[rock_row + 1][col] = (
                        platform[rock_row + 1][col],
                        platform[rock_row][col],
                    )
    total_load: int = 0
    for row in range(len(platform)):
        for col in range(len(platform[0])):
            if platform[row][col] == "O":
                total_load += len(platform) - row

    return total_load


if __name__ == "__main__":
    print(solution("./example.txt"))  # 136
    print(solution("./input.txt"))  # 110090
