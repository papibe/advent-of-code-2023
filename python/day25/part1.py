from collections import defaultdict, deque
from typing import DefaultDict, Deque, Dict, List, Set, Tuple


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    all_components: Dict[str, bool] = {}
    connections: Dict[str, List[str]] = {}
    for line in data:
        main_component, rest = line.split(": ")
        other_components: List[str] = rest.split(" ")
        all_components[main_component] = True
        for other_component in other_components:
            all_components[other_component] = True

        connections[main_component] = other_components

    adjacency_list: DefaultDict[int, List[int]] = defaultdict(list)

    components: List[str] = list(all_components.keys())
    byjection: Dict[str, int] = {}
    for index, component in enumerate(components):
        byjection[component] = index

    for node, connected_nodes in connections.items():
        for connected_node in connected_nodes:
            adjacency_list[byjection[node]].append(byjection[connected_node])
            adjacency_list[byjection[connected_node]].append(byjection[node])

    size: int = len(all_components)

    counter: DefaultDict[Tuple[int, int], int] = defaultdict(int)

    for source in range(size):
        q: Deque[int] = deque([source])
        visited: Set[int] = set([source])
        previous: Dict[int, int] = {}
        while q:
            node_: int = q.popleft()

            for next_node in adjacency_list[node_]:
                if next_node not in visited:
                    previous[next_node] = node_
                    q.append(next_node)
                    visited.add(next_node)

        for node_ in range(size):
            while node_ != source:
                prev: int = previous[node_]
                counter[(min(node_, prev), max(node_, prev))] += 1
                node_ = prev

    top_nodes: List[Tuple[Tuple[int, int], int]] = sorted(
        counter.items(), key=lambda x: x[1], reverse=True
    )

    node1: int
    node2: int
    for (node1, node2), _ in top_nodes[:3]:
        adjacency_list[node1].remove(node2)
        adjacency_list[node2].remove(node1)

    source = 0
    queue: Deque[int] = deque([source])
    visited = set([source])
    while queue:
        node_ = queue.popleft()
        for next_node in adjacency_list[node_]:
            if next_node not in visited:
                queue.append(next_node)
                visited.add(next_node)

    return len(visited) * (size - len(visited))


if __name__ == "__main__":
    print(solution("./example.txt"))  # 54
    print(solution("./input.txt"))  # 543564
