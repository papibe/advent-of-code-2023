import re
from typing import List, Match, Optional


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    line_regex: str = r"Card\s+\d+: ([^|]*) \| ([^|]*)"
    num_regex: str = r"\d+"
    total_points: int = 0

    for line in data:
        matches: Optional[Match[str]] = re.search(line_regex, line)
        assert matches is not None
        wining = {n for n in re.findall(num_regex, matches.group(1))}

        points: int = 0
        for my_card in re.findall(num_regex, matches.group(2)):
            if my_card in wining:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        total_points += points

    return total_points


if __name__ == "__main__":
    print(solution("./example.txt"))  # 13
    print(solution("./input.txt"))  # 20855
