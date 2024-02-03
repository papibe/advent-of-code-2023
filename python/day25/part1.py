from collections import deque, defaultdict
from itertools import combinations
from copy import deepcopy


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    all_components = {}
    connections = {}
    for line in data:
        main_component, rest = line.split(": ")
        other_components = rest.split(" ")
        all_components[main_component] = True
        for other_component in other_components:
            all_components[other_component] = True

        connections[main_component] = other_components

    al = defaultdict(list)

    components = list(all_components.keys())
    cm = {}
    for index, component in enumerate(components):
        cm[component] = index

    for node, connected_nodes in connections.items():
        for connected_node in connected_nodes:
            al[cm[node]].append(cm[connected_node])
            al[cm[connected_node]].append(cm[node])

    size = len(all_components)

    counter = defaultdict(int)

    for source in range(size):
        q = deque([source])
        visited = set([source])
        previous = {}
        while q:
            node = q.popleft()

            for next_node in al[node]:
                if next_node not in visited:
                    # counter[(min(node, next_node), max(node, next_node))] += 1
                    previous[next_node] = node
                    q.append(next_node)
                    visited.add(next_node)

        for node in range(size):
            while node != source:
                prev = previous[node]
                counter[(min(node, prev), max(node, prev))] += 1
                node = prev

    top_nodes = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    # for (n1, n2), count in top_nodes[:7]:
    #     print(components[n1], components[n2], count)

    for (n1, n2), _ in top_nodes[:3]:
        al[n1].remove(n2)
        al[n2].remove(n1)

    source = 0
    q = deque([source])
    visited = set([source])
    while q:
        node = q.popleft()
        for next_node in al[node]:
            if next_node not in visited:
                q.append(next_node)
                visited.add(next_node)

    return len(visited) * (size - len(visited))


if __name__ == "__main__":
    print(solution("./example.txt"))  # 54
    print(solution("./input.txt"))  # 543564
