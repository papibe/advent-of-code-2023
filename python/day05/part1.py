import re
from typing import Dict, List


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read()

    num_regex: str = r"\d+"

    blocks: List[str] = data.split("\n\n")
    seeds: List[int] = [
        int(str_n) for str_n in re.findall(num_regex, blocks[0].splitlines()[0])
    ]

    almanac: Dict[int, List[Dict[str, int]]] = {}

    for map_number, block in enumerate(data.split("\n\n")[1:]):
        list_of_ranges: List[Dict[str, int]] = []
        for line in block.splitlines()[1:]:
            numbers: List[int] = [
                int(str_n) for str_n in re.findall(num_regex, line.splitlines()[0])
            ]
            d: Dict[str, int] = {}
            d["start"] = numbers[1]
            d["len_"] = numbers[2]
            d["end"] = numbers[1] + numbers[2] - 1
            d["trans"] = numbers[0]
            list_of_ranges.append(d)
        almanac[map_number] = list_of_ranges

    min_location: int = float("inf")  # type: ignore[assignment]
    for seed in seeds:
        for _, lor in almanac.items():
            for d in lor:
                if d["start"] <= seed <= d["end"]:
                    seed = d["trans"] + seed - d["start"]
                    break
        min_location = min(min_location, seed)

    return min_location


if __name__ == "__main__":
    print(solution("./example.txt"))  # 35
    print(solution("./input.txt"))  #   3374647
