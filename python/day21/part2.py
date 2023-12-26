import re
from collections import deque

LAST = -1

def garden_count(start_row, start_col, garden):
    # please let if be square ;-)
    assert len(garden) == len(garden[0])
    size = len(garden)

    # row, col, distance
    queue = deque([(start_row, start_col, 0)])
    visited = set([start_row, start_col])

    distances = [[None] * size for _ in range(size)]

    while queue:
        row, col, current_distance = queue.popleft()

        distances[row][col] = current_distance

        # RIGHT, LEFT, UP, DOWN
        direction_steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for step_row, step_col in direction_steps:
            new_row = row + step_row
            new_col = col + step_col
            new_distance = current_distance + 1
            if 0 <= new_row < size and 0 <= new_col < size:
                if (
                    garden[new_row][new_col] == "."
                    and (new_row, new_col) not in visited
                ):
                    queue.append((new_row, new_col, new_distance))
                    visited.add((new_row, new_col))

    return distances



def solution(filename: str, max_total_steps) -> int:
    with open(filename, "r") as fp:
        garden: str = fp.read().splitlines()

    for row, line in enumerate(garden):
        for col, cell in enumerate(line):
            if cell == "S":
                start_row = row
                start_col = col
                break
        else:
            continue
        break

    parity = max_total_steps % 2
    size = len(garden)

    distances = garden_count(start_row, start_col, garden)

    shortest_distance_to_right = min([distances[row][LAST] for row in range(size)])
    shortest_distance_to_left = min([distances[row][0] for row in range(size)])
    shortest_distance_to_top = min([distances[0][col] for col in range(size)])
    shortest_distance_to_bottom = min([distances[LAST][col] for row in range(size)])

    shortest_distance_to_edges = shortest_distance_to_right
    # print(shortest_distance_to_edges)

    # for input only
    assert shortest_distance_to_edges == shortest_distance_to_right
    assert shortest_distance_to_edges == shortest_distance_to_left
    assert shortest_distance_to_edges == shortest_distance_to_top
    assert shortest_distance_to_edges == shortest_distance_to_bottom

    diameter = (max_total_steps - shortest_distance_to_edges) // size
    # print(diameter)

    odd_grid = even_grid = odd_corner = even_corner = 0
    for row in distances:
        for distance in row:
            if distance is None:
                continue
            if distance % 2 == 0:
                even_grid += 1
                if distance > shortest_distance_to_edges:
                    even_corner += 1
            else:
                odd_grid += 1
                if distance > shortest_distance_to_edges:
                    odd_corner += 1

    # to obtain this formula spend some time on a whiteboard going
    # from small cases to big cases (diameter) and you'll find a pattern :-)
    return (
        ((diameter + 1) ** 2) * odd_grid
        + (diameter **2) * even_grid
        - (diameter + 1) * odd_corner
        + diameter * even_corner
    )

if __name__ == "__main__":
    print(solution("./input.txt", 26501365))  # 609012263058042
