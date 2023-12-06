#
# working draft. will clean up
#
import re


def proc_range(almanac, intervals):
    rule_n = -1
    for _, lor in almanac.items():
        rule_n += 1
        rule_output = []
        while intervals:
            print(f"{intervals = }")
            a, b = intervals.pop()
            apply_rule = -1
            for rn, rule_d in enumerate(lor):
                # print(f"{(a, b) = }")
                # print(f"{intervals = }")
                c, d = rule_d["start"], rule_d["end"]

                if b < c or d < a:
                    # rule_output.append([a, b])
                    continue
                apply_rule = rn
                # break

                # if apply_rule == -1:
                #     rule_output.append([a, b])
                #     # break
                #     continue

                print(f"applying rule {rule_n}->{apply_rule}")
                c, d = lor[apply_rule]["start"], lor[apply_rule]["end"]

                i_s = max(a, c)
                i_e = min(b, d)

                if i_s < i_e:
                    t_s = lor[apply_rule]["trans"] + i_s - lor[apply_rule]["start"]
                    t_e = lor[apply_rule]["trans"] + i_e - lor[apply_rule]["start"]
                    print(f"{rule_n = }, {(i_s, i_e) = } -> {(t_s, t_e) = }")
                    rule_output.append([t_s, t_e])

                    if i_s > a:
                        intervals.append([a, i_s])
                    if b > i_e:
                        intervals.append([i_e, b])
                    break
            else:
                rule_output.append([a, b])

            # end of rule
        intervals = rule_output

    return intervals


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read()

    num_regex = r"\d+"

    blocks = data.split("\n\n")
    seeds = [int(str_n) for str_n in re.findall(num_regex, blocks[0].splitlines()[0])]
    # print(seeds)

    almanac = {}

    for map_number, block in enumerate(data.split("\n\n")[1:]):
        # almanac[map_number] =
        list_of_ranges = []
        for line in block.splitlines()[1:]:
            numbers = [
                int(str_n) for str_n in re.findall(num_regex, line.splitlines()[0])
            ]
            d = {}
            d["start"] = numbers[1]
            d["len_"] = numbers[2]
            # d["end"] = numbers[1] + numbers[2] - 1
            d["end"] = numbers[1] + numbers[2]
            d["trans"] = numbers[0]
            list_of_ranges.append(d)
        almanac[map_number] = list_of_ranges

    seed_intervals = []
    for index, seed_start in enumerate(seeds):
        if index % 2 != 0:
            continue
        seed_intervals.append([seed_start, seed_start + seeds[index + 1]])

    # print(seed_intervals)

    results = []
    for (start, end) in seed_intervals:
        # result = proc_range(almanac, [[82, 83]])
        result = proc_range(almanac, [[start, end]])
        results.extend(result)
        # break

    print("=" * 60)
    print(results)
    return min([value for (value, _) in results])


if __name__ == "__main__":
    # print(solution("./example.txt"))  # 46
    print(solution("./input.txt"))  # to high 7623322 7623321 7623319
