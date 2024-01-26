from collections import deque
from typing import Deque, List, Set, Tuple

GARDEN_PLOT: str = "."

Coords = Tuple[int, int]


def solution(filename: str, max_total_steps: int) -> int:
    with open(filename, "r") as fp:
        garden: List[str] = fp.read().splitlines()

    for row, line in enumerate(garden):
        for col, cell in enumerate(line):
            if cell == "S":
                start_row = row
                start_col = col
                break
        else:
            continue
        break

    parity: int = max_total_steps % 2
    size: int = len(garden)

    queue: Deque[Tuple[int, int, int]] = deque(
        [(start_row, start_col, max_total_steps)]
    )
    visited: Set[Coords] = set([(start_row, start_col)])
    counter: int = 0

    while queue:
        row, col, steps = queue.popleft()

        if steps < 0:
            continue

        if steps % 2 == parity:
            counter += 1

        if steps == 0:
            continue

        # RIGHT, LEFT, UP, DOWN
        direction_steps: List[Coords] = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for step_row, step_col in direction_steps:
            new_row: int = row + step_row
            new_col: int = col + step_col
            new_steps: int = steps - 1
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
