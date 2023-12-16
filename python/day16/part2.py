from collections import deque

RIGHT = (0, 1)
LEFT = (0, -1)
UP = (-1, 0)
DOWN = (1, 0)

RULES = {
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
        contraption: str = fp.read().splitlines()

    max_energy = 0
    for col in range(len(contraption[0])):
        max_energy = max(max_energy, solve(contraption, (0, col), DOWN))
        max_energy = max(
            max_energy, solve(contraption, (len(contraption) - 1, col), UP)
        )

    for row in range(len(contraption)):
        max_energy = max(max_energy, solve(contraption, (row, 0), LEFT))
        max_energy = max(
            max_energy, solve(contraption, (row, len(contraption[0]) - 1), RIGHT)
        )

    return max_energy


def solve(contraption, position, direction) -> int:

    visited = set()
    queue = deque([(position, direction)])
    energized = set()
    while queue:
        pos, direction = queue.popleft()
        energized.add(pos)

        cell = contraption[pos[0]][pos[1]]

        next_directions = RULES[direction][cell]

        for dir in next_directions:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if (
                0 <= new_pos[0] < len(contraption)
                and 0 <= new_pos[1] < len(contraption[0])
                and (new_pos, dir) not in visited
            ):
                queue.append((new_pos, dir))
                visited.add((new_pos, dir))

    return len(energized)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 51
    print(solution("./input.txt"))  # 7987
