from collections import deque
from typing import Deque, Dict, List, Set, Tuple

Direction = Tuple[int, int]
Position = Tuple[int, int]

RIGHT: Direction = (0, 1)
LEFT: Direction = (0, -1)
UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)

RULES: Dict[Direction, Dict[str, List[Direction]]] = {
    RIGHT: {
        ".": [RIGHT],
        "/": [UP],
        "\\": [DOWN],
        "|": [UP, DOWN],
        "-": [RIGHT],
    },
    LEFT: {
        ".": [LEFT],
        "/": [DOWN],
        "\\": [UP],
        "|": [UP, DOWN],
        "-": [LEFT],
    },
    UP: {
        ".": [UP],
        "/": [RIGHT],
        "\\": [LEFT],
        "|": [UP],
        "-": [LEFT, RIGHT],
    },
    DOWN: {
        ".": [DOWN],
        "/": [LEFT],
        "\\": [RIGHT],
        "|": [DOWN],
        "-": [LEFT, RIGHT],
    },
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        contraption: List[str] = fp.read().splitlines()

    visited: Set[Tuple[Position, Direction]] = set()
    queue: Deque[Tuple[Position, Direction]] = deque([((0, 0), RIGHT)])
    energized: Set[Position] = set()

    while queue:
        pos, direction = queue.popleft()
        energized.add(pos)

        cell: str = contraption[pos[0]][pos[1]]

        next_directions: List[Direction] = RULES[direction][cell]

        for dir in next_directions:
            new_pos: Position = (pos[0] + dir[0], pos[1] + dir[1])
            if (
                0 <= new_pos[0] < len(contraption)
                and 0 <= new_pos[1] < len(contraption[0])
                and (new_pos, dir) not in visited
            ):
                queue.append((new_pos, dir))
                visited.add((new_pos, dir))

    return len(energized)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 46
    print(solution("./input.txt"))  # 7788
