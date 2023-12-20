import re
from collections import deque


STEPS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    regex = r"(\w+) (\w+) \(#(\w+)\)"

    row, col = (0, 0)
    edges = set([(0, 0)])

    for line in data:
        match = re.search(regex, line)

        direction = match.group(1)
        amount = int(match.group(2))
        color = match.group(3)

        for step in range(amount):
            row += STEPS[direction][0]
            col += STEPS[direction][1]
            edges.add((row, col))

    min_row = float("inf")
    max_row = float("-inf")
    min_col = float("inf")
    max_col = float("-inf")
    for (row, col) in edges:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    inside = set()

    queue = deque([(1, 1, 0)])
    visited = set([(1, 1)])
    while queue:
        row, col, count = queue.popleft()
        inside.add((row, col))

        # RIGHT, LEFT, UP, DOWN
        steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        for step_row, step_col in steps:
            new_row = row + step_row
            new_col = col + step_col

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
