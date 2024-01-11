import math
import re
from typing import Dict, List, Match


def lcm(a: int, b: int) -> int:
    return (a * b) // math.gcd(a, b)


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    directions: str = data[0]
    regex: str = r"(\w+) = \((\w+), (\w+)\)"

    network: Dict[str, Dict[str, str]] = {}

    for line in data[2:]:
        matches: Match[str] | None = re.search(regex, line)
        assert matches is not None
        network[matches.group(1)] = {"L": matches.group(2), "R": matches.group(3)}

    starting_positions: List[str] = []
    for position in network:
        if position.endswith("A"):
            starting_positions.append(position)

    path_info: List[Dict[str, int]] = []
    for position in starting_positions:
        seen: Dict[str, int] = {}
        index: int = 0
        counter: int = 0
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

    current_lcm: int = 1
    for cycle in path_info:
        current_lcm = lcm(current_lcm, cycle["cycle"])

    return current_lcm


if __name__ == "__main__":
    print(solution("./example3.txt"))  # 6
    print(solution("./input.txt"))  # 12357789728873
