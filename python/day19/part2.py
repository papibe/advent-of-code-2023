import re
from collections import deque
from copy import deepcopy
from typing import Deque, Dict, List, Match, Optional, Tuple


class Workflow:
    def __init__(self) -> None:
        self.rules: List[Rule] = []
        self.final: str = ""


class Rule:
    def __init__(self, attr: str, comp: str, value: int, workflow: str) -> None:
        self.attr: str = attr
        self.comp: str = comp
        self.value: int = value
        self.workflow: str = workflow

    def values(self) -> Tuple[str, str, int, str]:
        return (self.attr, self.comp, self.value, self.workflow)


Parts = Dict[str, List[int]]


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    workflows_str: List[str] = blocks[0].splitlines()
    workflows: Dict[str, Workflow] = {}

    wf_regex: str = r"(\w+){(.*)}"
    rule_regex: str = r"(\w)([><])(\d+):(\w+)"

    # parse rules
    for line in workflows_str:
        matches: Optional[Match[str]] = re.search(wf_regex, line)

        assert matches is not None
        name: str = matches.group(1)
        rules: List[str] = matches.group(2).split(",")
        workflows[name] = Workflow()

        for rule in rules:
            matches = re.search(rule_regex, rule)
            if matches:
                attr: str = matches.group(1)
                comp: str = matches.group(2)
                value: int = int(matches.group(3))
                workflow: str = matches.group(4)

                workflows[name].rules.append(Rule(attr, comp, value, workflow))
            else:
                workflows[name].final = rule

    part: Parts = {
        "x": [1, 4000],
        "m": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
    }
    queue: Deque[Tuple[str, Dict[str, List[int]]]] = deque([("in", part)])
    accepted_parts = []

    # apply rules in a BFS-style
    while queue:
        wf, part = queue.popleft()

        if wf == "R":
            continue
        if wf == "A":
            accepted_parts.append(part)
            continue

        for rule_ in workflows[wf].rules:
            attr, comp, value, workflow = rule_.values()
            if comp == "<":
                new_part: Parts = deepcopy(part)
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
                raise Exception("something went wrong")

        if all(lower <= upper for lower, upper in part.values()):
            queue.append((workflows[wf].final, part.copy()))

    # calculate possibilities
    total_sum: int = 0
    for part in accepted_parts:
        total: int = 1
        for lower, upper in part.values():
            if upper >= lower:
                total *= upper - lower + 1
        total_sum += total
    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 167409079868000
    print(solution("./input.txt"))  # 133973513090020
