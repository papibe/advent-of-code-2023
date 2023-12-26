import re
from collections import deque

GARDEN_PLOT = "."


def solution(filename: str, max_total_steps) -> int:
    with open(filename, "r") as fp:
        garden: str = fp.read().splitlines()

    for row, line in enumerate(garden):
        for col, cell in enumerate(line):
            if cell == "S":
                start_row = row
                start_col = col
                break
        else:
            continue
        break

    parity = max_total_steps % 2
    size = len(garden)

    queue = deque([(start_row, start_col, max_total_steps)])
    visited = set([start_row, start_col])
    counter = 0

    while queue:
        row, col, steps = queue.popleft()

        if steps < 0:
            continue

        if steps % 2 == parity:
            counter += 1

        if steps == 0:
            continue

        # RIGHT, LEFT, UP, DOWN
        direction_steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for step_row, step_col in direction_steps:
            new_row = row + step_row
            new_col = col + step_col
            new_steps = steps - 1
            if 0 <= new_row < size and 0 <= new_col < size:
                if (
                    new_steps >= 0
                    and garden[new_row][new_col] == "."
                    and (new_row, new_col) not in visited
                ):
                    queue.append((new_row, new_col, new_steps))
                    visited.add((new_row, new_col))

    return counter


if __name__ == "__main__":
    print(solution("./example.txt", 6))  # 16
    print(solution("./input.txt", 64))  # 3682
