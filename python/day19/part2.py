import re
from collections import deque
from copy import deepcopy


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        blocks: str = fp.read().split("\n\n")

    workflows_str = blocks[0].splitlines()
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

    part = {
        "x": [1, 4000],
        "m": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
    }
    queue = deque([("in", part)])
    accepted_parts = []

    # apply rules in a BFS-style
    while queue:
        wf, part = queue.popleft()

        if wf == "R":
            continue
        if wf == "A":
            accepted_parts.append(part)
            continue

        for rule in workflows[wf]["rules"]:
            attr, comp, value, workflow = rule.values()
            if comp == "<":
                new_part = deepcopy(part)
                new_part[attr][1] = min(new_part[attr][1], value - 1)
                if part[attr][0] <= part[attr][1]:
                    queue.append((workflow, new_part))
                part[attr][0] = max(part[attr][0], value)
            elif comp == ">":
                new_part = deepcopy(part)
                new_part[attr][0] = max(new_part[attr][0], value + 1)
                if part[attr][0] <= part[attr][1]:
                    queue.append((workflow, new_part))
                part[attr][1] = min(part[attr][1], value)
            else:
                raise ("blah")

        if all(lower <= upper for lower, upper in part.values()):
            queue.append((workflows[wf]["finally"], part.copy()))

    # calculate possibilities
    total_sum = 0
    for part in accepted_parts:
        total = 1
        for lower, upper in part.values():
            if upper >= lower:
                total *= upper - lower + 1
        total_sum += total
    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 167409079868000
    print(solution("./input.txt"))  # 133973513090020
