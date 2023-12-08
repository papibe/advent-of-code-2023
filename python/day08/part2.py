import re
from collections import deque
import math


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    directions = data[0]
    regex = r"(\w+) = \((\w+), (\w+)\)"

    network = {}

    for line in data[2:]:
        match = re.search(regex, line)
        network[match.group(1)] = {"L": match.group(2), "R": match.group(3)}

    starting_positions = []
    for position in network:
        if position.endswith("A"):
            starting_positions.append(position)

    path_info = []
    for position in starting_positions:
        seen = {}
        index = 0
        counter = 0
        seen[position] = counter

        while True:
            position = network[position][directions[index]]
            index = (index + 1) % len(directions)
            counter += 1

            if position in seen and position.endswith("Z"):
                path_info.append(
                    {"prefix": seen[position], "cycle": counter - seen[position]}
                )
                break
            else:
                seen[position] = counter

    def lcm(a, b):
        return (a * b) // math.gcd(a, b)

    current_lcm = 1
    for cycle in path_info:
        current_lcm = lcm(current_lcm, cycle["cycle"])

    return current_lcm


if __name__ == "__main__":
    print(solution("./example3.txt"))  # 6
    print(solution("./input.txt"))  # 12357789728873
