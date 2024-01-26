from collections import deque
from typing import Deque, List, Set, Tuple

GARDEN_PLOT: str = "."

Coords = Tuple[int, int]


def solution(filename: str, max_steps: int) -> int:
    with open(filename, "r") as fp:
        garden: List[str] = fp.read().splitlines()

    for row, line in enumerate(garden):
        for col, cell in enumerate(line):
            if cell == "S":
                break
        else:
            continue
        break

    coords: Set[Coords] = set([(row, col)])
    queue: Deque[Tuple[Set[Coords], int]] = deque([(coords, 0)])
    while queue:
        coords, steps_count = queue.popleft()

        if steps_count == max_steps:
            break

        # RIGHT, LEFT, UP, DOWN
        steps: List[Coords] = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        next_coords: Set[Coords] = set()
        for (row, col) in coords:
            for step_row, step_col in steps:
                new_row: int = row + step_row
                new_col: int = col + step_col
                if 0 <= new_row < len(garden) and 0 <= new_col < len(garden[0]):
                    if garden[new_row][new_col] == "#":
                        continue
                    next_coords.add((new_row, new_col))
        queue.append((next_coords, steps_count + 1))

    return len(coords)


if __name__ == "__main__":
    print(solution("./example.txt", 6))  # 16
    print(solution("./input.txt", 64))  # 3682
