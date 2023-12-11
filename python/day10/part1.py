import re
from collections import deque


landscape = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(1, 0), (0, 1)],
    ".": [],
    "S": [(1, 0), (-1, 0)],
    # "S":[(1, 0), (0, 1)],
}

START = "S"


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    # find start
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == START:
                break
        else:
            continue
        break
    # print(row, col)

    queue = deque([(row, col, 0)])
    visited = set([(row, col)])

    counted = []
    for line in data:
        counted.append([char for char in line])

    max_steps = 0
    while queue:
        row, col, steps = queue.popleft()
        counted[row][col] = str(steps)
        # for line in counted:
        #     print(line)
        # print("-------------------------------------")
        max_steps = max(max_steps, steps)

        for (nrow, ncol) in landscape[data[row][col]]:
            new_row = row + nrow
            new_col = col + ncol
            if 0 <= new_row <= len(data) and 0 <= new_col < len(data[0]):

                if data[row][col] != "." and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))

    return max_steps


if __name__ == "__main__":
    # print(solution("./example1.txt"))  #
    # print(solution("./example2.txt"))  #
    print(solution("./input.txt"))  #
