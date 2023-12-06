import re


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read()

    num_regex = r"\d+"

    blocks = data.split("\n\n")
    seeds = [int(str_n) for str_n in re.findall(num_regex, blocks[0].splitlines()[0])]

    almanac = {}

    for map_number, block in enumerate(data.split("\n\n")[1:]):
        list_of_ranges = []
        for line in block.splitlines()[1:]:
            numbers = [
                int(str_n) for str_n in re.findall(num_regex, line.splitlines()[0])
            ]
            d = {}
            d["start"] = numbers[1]
            d["len_"] = numbers[2]
            d["end"] = numbers[1] + numbers[2] - 1
            d["trans"] = numbers[0]
            list_of_ranges.append(d)
        almanac[map_number] = list_of_ranges

    min_location = float("inf")
    for seed in seeds:
        for _, lor in almanac.items():
            for d in lor:
                if d["start"] <= seed <= d["end"]:
                    seed = d["trans"] + seed - d["start"]
                    break
        min_location = min(min_location, seed)

    return min_location


if __name__ == "__main__":
    # print(solution("./example.txt"))  #
    print(solution("./input.txt"))  #
