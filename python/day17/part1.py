import heapq as hq


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        city_map: str = fp.read().splitlines()

    # heat, row, col, dir_row, dir_col, strait steps
    queue = [(0, 0, 0, 0, 0, 0)]
    hq.heapify(queue)
    visited = set((0, 0, 0, 0, 0))
    destination = (len(city_map) - 1, len(city_map[0]) - 1)

    while queue:
        heat, row, col, dir_row, dir_col, s_steps = hq.heappop(queue)

        if (row, col) == destination:
            return heat

        # RIGHT, LEFT, UP, DOWN
        steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        for step_row, step_col in steps:
            new_row = row + step_row
            new_col = col + step_col

            if 0 <= new_row < len(city_map) and 0 <= new_col < len(city_map[0]):
                # can't go back on opposite direction
                if (step_row, step_col) == (-dir_row, -dir_col):
                    continue

                # if we already took 3 steps don't continue in this direction
                if (step_row, step_col) == (dir_row, dir_col) and s_steps >= 3:
                    continue

                # Same direction: increase steps, if not reset steps
                if (step_row, step_col) == (dir_row, dir_col):
                    new_steps = s_steps + 1
                else:
                    new_steps = 1

                if (new_row, new_col, step_row, step_col, new_steps) in visited:
                    continue

                new_heat = heat + int(city_map[new_row][new_col])
                hq.heappush(
                    queue,
                    (new_heat, new_row, new_col, step_row, step_col, new_steps),
                )
                visited.add((new_row, new_col, step_row, step_col, new_steps))

    print("possible failure")
    return -1


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 102
    print(solution("./input.txt"))  # 1256
