import re
from typing import Dict, List, Match, Optional

MAX_CUBES: Dict[str, int] = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    game_id_sum: int = 0
    line_re: str = r"Game (\d+): (.*)$"

    for line in data:
        matches: Optional[Match[str]] = re.search(line_re, line)
        assert matches is not None
        game_number: int = int(matches.group(1))
        all_subsets: str = matches.group(2)

        subsets: List[str] = all_subsets.split("; ")
        for cube_set in subsets:
            cubes: List[str] = cube_set.split(", ")
            game_cubes: Dict[str, int] = {}

            for cube in cubes:
                number, color = cube.split(" ")
                game_cubes[color] = game_cubes.get(color, 0) + int(number)

            for color, quantity in game_cubes.items():
                if quantity > MAX_CUBES[color]:
                    break
            else:
                continue
            break
        else:
            game_id_sum += game_number
            continue

    return game_id_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 8
    print(solution("./input.txt"))  # 2156
