#
# working draft. will clean up
#
import re
from typing import Dict, List


def proc_range(
    almanac: Dict[int, List[Dict[str, int]]], intervals: List[List[int]]
) -> List[List[int]]:
    rule_n: int = -1
    for _, lor in almanac.items():
        rule_n += 1
        rule_output: List[List[int]] = []
        while intervals:
            a, b = intervals.pop()
            apply_rule: int = -1
            for rn, rule_d in enumerate(lor):
                c, d = rule_d["start"], rule_d["end"]

                if b < c or d < a:
                    continue
                apply_rule = rn

                c, d = lor[apply_rule]["start"], lor[apply_rule]["end"]

                i_s: int = max(a, c)
                i_e: int = min(b, d)

                if i_s < i_e:
                    t_s = lor[apply_rule]["trans"] + i_s - lor[apply_rule]["start"]
                    t_e = lor[apply_rule]["trans"] + i_e - lor[apply_rule]["start"]
                    rule_output.append([t_s, t_e])

                    if i_s > a:
                        intervals.append([a, i_s])
                    if b > i_e:
                        intervals.append([i_e, b])
                    break
            else:
                rule_output.append([a, b])

        intervals = rule_output

    return intervals


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
            numbers = [
                int(str_n) for str_n in re.findall(num_regex, line.splitlines()[0])
            ]
            d: Dict[str, int] = {}
            d["start"] = numbers[1]
            d["len_"] = numbers[2]
            d["end"] = numbers[1] + numbers[2]
            d["trans"] = numbers[0]
            list_of_ranges.append(d)
        almanac[map_number] = list_of_ranges

    seed_intervals: List[List[int]] = []
    for index, seed_start in enumerate(seeds):
        if index % 2 != 0:
            continue
        seed_intervals.append([seed_start, seed_start + seeds[index + 1]])

    results: List[List[int]] = []
    for (start, end) in seed_intervals:
        result = proc_range(almanac, [[start, end]])
        results.extend(result)

    return min([value for (value, _) in results])


if __name__ == "__main__":
    print(solution("./example.txt"))  # 46
    print(solution("./input.txt"))  # 6082852
