from collections import deque
from copy import deepcopy


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    rules = {
        (0, 1): ">",
        (0, -1): "<",
        (-1, 0): "^",
        (1, 0): "v",
    }
    goal = (len(data) - 1, len(data[0]) - 2)

    queue = deque([(0, 1, 0, set([(0, 1)]))])
    max_distance = 0

    while queue:
        row, col, distance, visited = queue.popleft()
        if (row, col) == goal:
            print(distance)
            max_distance = max(max_distance, distance)

        # RIGHT, LEFT, UP, DOWN
        direction_steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for step_row, step_col in direction_steps:
            new_row = row + step_row
            new_col = col + step_col
            new_distance = distance + 1

            if not (0 <= new_row < len(data) and 0 <= new_col < len(data[0])):
                continue

            current = data[new_row][new_col]

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
