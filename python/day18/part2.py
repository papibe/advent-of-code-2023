import re
from typing import Dict, List, Match, Optional, Tuple

STEPS: Dict[str, Tuple[int, int]] = {
    "0": (0, 1),
    "2": (0, -1),
    "3": (-1, 0),
    "1": (1, 0),
}

# references
# https://en.wikipedia.org/wiki/Shoelace_formula
# https://en.wikipedia.org/wiki/Pick%27s_theorem


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    regex: str = r"(\w+) (\w+) \(#(\w+)\)"

    row, col = (0, 0)
    points: List[Tuple[int, int]] = [(0, 0)]

    boundary: int = 0

    for line in data:
        matches: Optional[Match[str]] = re.search(regex, line)

        assert matches is not None
        hex_digits: str = matches.group(3)
        amount: int = int(hex_digits[:5], 16)
        direction: str = hex_digits[-1]

        boundary += amount

        next_row: int = row + STEPS[direction][0] * amount
        next_col: int = col + STEPS[direction][1] * amount

        points.append((next_row, next_col))

        row, col = next_row, next_col

    area: int = 0
    for i in range(len(points) - 1):
        area += (points[i][1] + points[i + 1][1]) * (points[i][0] - points[i + 1][0])
    area = abs(area) // 2

    return (area - (boundary // 2) + 1) + boundary


if __name__ == "__main__":
    print(solution("./example.txt"))  # 952408144115
    print(solution("./input.txt"))  # 60612092439765
