import re
from collections import deque
from typing import Deque, Dict, List, Match, Optional, Set, Tuple

STEPS: Dict[str, Tuple[int, int]] = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    regex: str = r"(\w+) (\w+) \(#(\w+)\)"

    row, col = (0, 0)
    edges: Set[Tuple[int, int]] = set([(0, 0)])

    for line in data:
        matches: Optional[Match[str]] = re.search(regex, line)

        assert matches is not None
        direction: str = matches.group(1)
        amount: int = int(matches.group(2))
        # color: str = matches.group(3)

        for step in range(amount):
            row += STEPS[direction][0]
            col += STEPS[direction][1]
            edges.add((row, col))

    min_row: int = float("inf")  # type: ignore
    max_row: int = float("-inf")  # type: ignore
    min_col: int = float("inf")  # type: ignore
    max_col: int = float("-inf")  # type: ignore
    for (row, col) in edges:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    inside: Set[Tuple[int, int]] = set()

    queue: Deque[Tuple[int, int, int]] = deque([(1, 1, 0)])
    visited: Set[Tuple[int, int]] = set([(1, 1)])
    while queue:
        row, col, count = queue.popleft()
        inside.add((row, col))

        # RIGHT, LEFT, UP, DOWN
        steps: List[Tuple[int, int]] = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        for step_row, step_col in steps:
            new_row: int = row + step_row
            new_col: int = col + step_col

            if min_row <= new_row <= max_row and min_col <= new_col <= max_col:

                if (new_row, new_col) in edges:
                    continue
                if (new_row, new_col) in visited:
                    continue
                queue.append((new_row, new_col, count + 1))
                visited.add((new_row, new_col))
            else:
                print("no good")

    return len(edges) + len(inside)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 62
    print(solution("./input.txt"))  # 52035
