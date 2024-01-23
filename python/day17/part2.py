import heapq as hq
from typing import List, Set, Tuple

HeapItem = Tuple[int, int, int, int, int, int]
VisitedItem = Tuple[int, int, int, int, int]


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        city_map: List[str] = fp.read().splitlines()

    # heat, row, col, dir_row, dir_col, strait steps
    queue: List[HeapItem] = [(0, 0, 0, 0, 0, 0)]
    hq.heapify(queue)
    visited: Set[VisitedItem] = set([(0, 0, 0, 0, 0)])
    destination: Tuple[int, int] = (len(city_map) - 1, len(city_map[0]) - 1)

    while queue:
        heat, row, col, dir_row, dir_col, s_steps = hq.heappop(queue)

        # we not only need to arrive at destination, but also taken at least 4 steps
        if (row, col) == destination and s_steps >= 4:
            return heat

        # RIGHT, LEFT, UP, DOWN
        steps: List[Tuple[int, int]] = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        for step_row, step_col in steps:
            new_row: int = row + step_row
            new_col: int = col + step_col

            if 0 <= new_row < len(city_map) and 0 <= new_col < len(city_map[0]):
                # can't go back on opposite direction
                if (step_row, step_col) == (-dir_row, -dir_col):
                    continue

                # if we haven't take 4 steps yet don't change directions
                if (dir_row, dir_col) != (0, 0) and s_steps < 4:
                    if (dir_row, dir_col) != (step_row, step_col):
                        continue

                # if we already took 10 steps don't continue in this direction
                if (step_row, step_col) == (dir_row, dir_col) and s_steps >= 10:
                    continue

                new_steps: int
                # Same direction: increase steps, if not reset steps
                if (step_row, step_col) == (dir_row, dir_col):
                    new_steps = s_steps + 1
                else:
                    new_steps = 1

                if (new_row, new_col, step_row, step_col, new_steps) in visited:
                    continue

                new_heat: int = heat + int(city_map[new_row][new_col])
                hq.heappush(
                    queue,
                    (new_heat, new_row, new_col, step_row, step_col, new_steps),
                )
                visited.add((new_row, new_col, step_row, step_col, new_steps))

    print("possible failure")
    return -1


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 94
    print(solution("./example2.txt"))  # 71
    print(solution("./input.txt"))  # 1382
