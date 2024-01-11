import re
from typing import Dict, List, Match


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

    position: str = "AAA"
    index: int = 0
    counter: int = 0

    while position != "ZZZ":
        position = network[position][directions[index]]
        index = (index + 1) % len(directions)
        counter += 1

    return counter


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 2
    print(solution("./example2.txt"))  # 6
    print(solution("./input.txt"))  # 24253
