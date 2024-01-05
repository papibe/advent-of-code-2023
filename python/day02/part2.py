import re
from typing import Dict, List, Match, Optional


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    sum_of_powers: int = 0
    line_re: str = r"Game (\d+): (.*)$"

    for line in data:
        matches: Optional[Match[str]] = re.search(line_re, line)
        assert matches is not None
        all_sets: str = matches.group(2)
        sets: List[str] = all_sets.split("; ")

        max_cubes: Dict[str, int] = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for cube_set in sets:
            cubes: List[str] = cube_set.split(", ")
            game_cubes: Dict[str, int] = {}

            for cube in cubes:
                number, color = cube.split(" ")
                game_cubes[color] = game_cubes.get(color, 0) + int(number)

            for color, quantity in game_cubes.items():
                max_cubes[color] = max(max_cubes[color], quantity)

            power: int = 1
            for quantity in max_cubes.values():
                power *= quantity

        sum_of_powers += power

    return sum_of_powers


if __name__ == "__main__":
    print(solution("./example.txt"))  # 2286
    print(solution("./input.txt"))  # 66909
