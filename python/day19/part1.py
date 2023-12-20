import re
from collections import deque


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        blocks: str = fp.read().split("\n\n")

    workflows_str = blocks[0].splitlines()
    parts_str = blocks[1].splitlines()

    workflows = {}
    wf_regex = r"(\w+){(.*)}"
    rule_regex = r"(\w)([><])(\d+):(\w+)"

    # parse rules
    for line in workflows_str:
        match = re.search(wf_regex, line)
        name = match.group(1)
        rules = match.group(2).split(",")

        workflows[name] = {"rules": [], "finally": ""}

        for rule in rules:
            match = re.search(rule_regex, rule)
            if match:
                attr = match.group(1)
                comp = match.group(2)
                value = int(match.group(3))

                wf = match.group(4)
                workflows[name]["rules"].append(
                    {
                        "attr": attr,
                        "comp": comp,
                        "value": value,
                        "workflow": wf,
                    }
                )
            else:
                workflows[name]["finally"] = rule

    parts = {}
    prop_regex = r"(\w)=(\d+)"

    # parse parts
    for part_number, line in enumerate(parts_str):
        attributes = line[1:-1].split(",")
        parts[part_number] = {}

        for attribute in attributes:
            match = re.search(prop_regex, attribute)
            attr = match.group(1)
            value = int(match.group(2))
            parts[part_number][attr] = value

    accepted_parts = []

    # apply rules to all parts
    for part_number, part in parts.items():
        wf = "in"

        while True:
            if wf == "R":
                break
            if wf == "A":
                accepted_parts.append(part_number)
                break

            for rule in workflows[wf]["rules"]:
                attr, comp, value, workflow = rule.values()
                if comp == "<":
                    if part[attr] < value:
                        wf = rule["workflow"]
                        break
                else:
                    if part[attr] > value:
                        wf = rule["workflow"]
                        break
            else:
                wf = workflows[wf]["finally"]

    # calculate sum of attributes
    total_sum = 0
    for part_number in accepted_parts:
        for k, v in parts[part_number].items():
            total_sum += v

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 19114
    print(solution("./input.txt"))  # 398527
