from collections import deque
from typing import Deque, Dict, List, Set, Tuple

Coords = Tuple[int, int]


RULES: Dict[Coords, str] = {
    (0, 1): ">",
    (0, -1): "<",
    (-1, 0): "^",
    (1, 0): "v",
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    start: Coords = (0, 1)
    goal: Coords = (len(data) - 1, len(data[0]) - 2)

    ############################################################################
    # get nodes a.k.a. forks, bifurcations
    ############################################################################
    nodes: List[Coords] = []
    for row, line in enumerate(data):
        for col, cell in enumerate(line):
            if cell != "#":
                direction_steps: List[Coords] = [(0, 1), (0, -1), (-1, 0), (1, 0)]
                bifurcations: int = 0
                for step_row, step_col in direction_steps:
                    new_row: int = row + step_row
                    new_col: int = col + step_col
                    if (
                        0 <= new_row < len(data)
                        and 0 <= new_col < len(data[0])
                        and data[new_row][new_col] != "#"
                    ):
                        bifurcations += 1
                if bifurcations > 2:
                    nodes.append((row, col))

    nodes.append(start)
    nodes.append(goal)

    ############################################################################
    def children_distance(
        start: Coords, visited: Set[Coords]
    ) -> List[Tuple[int, int, int]]:
        queue: Deque[Tuple[int, int, int]] = deque([(start[0], start[1], 0)])
        visited.add((start[0], start[1]))

        children: List[Tuple[int, int, int]] = []

        while queue:
            row, col, distance = queue.popleft()
            if (row, col) != start and (row, col) in nodes:
                children.append((row, col, distance))

                continue

            # RIGHT, LEFT, UP, DOWN
            direction_steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]
            for step_row, step_col in direction_steps:
                new_row: int = row + step_row
                new_col: int = col + step_col
                new_distance: int = distance + 1

                if (
                    0 <= new_row < len(data)
                    and 0 <= new_col < len(data[0])
                    and data[new_row][new_col] != "#"
                    and (new_row, new_col) not in visited
                ):
                    current = data[new_row][new_col]
                    if current != "." and current != RULES[(step_row, step_col)]:
                        continue
                    queue.append((new_row, new_col, new_distance))
                    visited.add((new_row, new_col))

        return children

    ############################################################################

    ############################################################################
    # create a new compress graph from previous nodes
    ############################################################################
    nodes_d: Dict[Coords, List[Tuple[int, int, int]]] = {node: [] for node in nodes}
    for node in nodes:
        nodes_d[node] = children_distance(node, set())

    ##########################################################################
    # final DFS
    ##########################################################################
    visited: Set[Coords] = set()

    def dfs(start: Coords, distance: int) -> int:
        if start == goal:
            return distance
        local_max: int = float("-inf")  # type: ignore
        visited.add(start)
        for row, col, new_distance in nodes_d[start]:
            if (row, col) not in visited:
                local_max = max(local_max, dfs((row, col), distance + new_distance))
        visited.remove(start)
        return local_max

    max_distance: int = dfs(start, 0)

    return max_distance


if __name__ == "__main__":
    print(solution("./example.txt"))  # 94
    print(solution("./input.txt"))  # 2298
