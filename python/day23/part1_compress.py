from collections import deque
from collections import defaultdict

RULES = {
    (0, 1): ">",
    (0, -1): "<",
    (-1, 0): "^",
    (1, 0): "v",
}

def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    start = (0, 1)
    goal = (len(data) - 1, len(data[0]) - 2)

    ############################################################################
    # get nodes a.k.a. forks, bifurcations
    ############################################################################
    nodes = []
    for row, line in enumerate(data):
        for col, cell in enumerate(line):
            if cell != "#":
                direction_steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]
                bifurcations = 0
                for step_row, step_col in direction_steps:
                    new_row = row + step_row
                    new_col = col + step_col
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
    def children_distance(start, visited):
        queue = deque([(start[0], start[1], 0)])
        # visited = set([(start[0], start[1])])
        visited.add((start[0], start[1]))

        children = []

        while queue:
            row, col, distance = queue.popleft()
            if (row, col) != start and (row, col) in nodes:
                children.append((row, col, distance))

                continue

            # RIGHT, LEFT, UP, DOWN
            direction_steps = [(0, 1), (0, -1), (-1, 0), (1, 0)]
            for step_row, step_col in direction_steps:
                new_row = row + step_row
                new_col = col + step_col
                new_distance = distance + 1

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
    nodes_d = {node: {} for node in nodes}
    for node in nodes:
        nodes_d[node] = children_distance(node, set())

    ##########################################################################
    # final DFS
    ##########################################################################
    visited = set()
    def dfs(start, distance):
        if start == goal:
            return distance
        local_max = float("-inf")
        visited.add(start)
        for row, col, new_distance in nodes_d[start]:
            if (row, col) not in visited:
                local_max = max(local_max, dfs((row, col), distance + new_distance))
        visited.remove(start)
        return local_max

    max_distance = dfs(start, 0)

    return max_distance


if __name__ == "__main__":
    print(solution("./example.txt"))  # 154
    print(solution("./input.txt"))  # 6602
