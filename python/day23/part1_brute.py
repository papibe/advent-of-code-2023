from collections import deque
from copy import deepcopy
from typing import Deque, Dict, List, Set, Tuple

Coords = Tuple[int, int]


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    rules: Dict[Coords, str] = {
        (0, 1): ">",
        (0, -1): "<",
        (-1, 0): "^",
        (1, 0): "v",
    }
    goal: Coords = (len(data) - 1, len(data[0]) - 2)

    queue: Deque[Tuple[int, int, int, Set[Coords]]] = deque([(0, 1, 0, set([(0, 1)]))])
    max_distance: int = 0

    while queue:
        row, col, distance, visited = queue.popleft()
        if (row, col) == goal:
            print(distance)
            max_distance = max(max_distance, distance)

        # RIGHT, LEFT, UP, DOWN
        direction_steps: List[Coords] = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for step_row, step_col in direction_steps:
            new_row: int = row + step_row
            new_col: int = col + step_col
            new_distance: int = distance + 1

            if not (0 <= new_row < len(data) and 0 <= new_col < len(data[0])):
                continue

            current: str = data[new_row][new_col]

            if current == "#":
                continue

            if (new_row, new_col) in visited:
                continue

            if current != "." and current != rules[(step_row, step_col)]:
                continue

            new_visited = deepcopy(visited)
            new_visited.add((new_row, new_col))
            queue.append((new_row, new_col, new_distance, new_visited))

    return max_distance


if __name__ == "__main__":
    print(solution("./example.txt"))  # 94
    print(solution("./input.txt"))  # 2298
