from collections import deque
from typing import Deque, Dict, List, Set, Tuple

landscape: Dict[str, List[Tuple[int, int]]] = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(1, 0), (0, 1)],
    ".": [],
    "S": [(1, 0), (-1, 0)],
}

START: str = "S"


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    # find start
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == START:
                start_row = row
                start_col = col
                break
        else:
            continue
        break

    queue: Deque[Tuple[int, int, int]] = deque([(start_row, start_col, 0)])
    visited: Set[Tuple[int, int]] = set([(start_row, start_col)])

    counted = []
    for line in data:
        counted.append([char for char in line])

    max_steps: int = 0
    while queue:
        row, col, steps = queue.popleft()
        counted[row][col] = str(steps)
        max_steps = max(max_steps, steps)

        for (nrow, ncol) in landscape[data[row][col]]:
            new_row: int = row + nrow
            new_col: int = col + ncol
            if 0 <= new_row < len(data) and 0 <= new_col < len(data[0]):

                if data[new_row][new_col] != "." and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))

    return len(visited) // 2


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 4
    print(solution("./example2.txt"))  # 8
    print(solution("./input.txt"))  # 6701
