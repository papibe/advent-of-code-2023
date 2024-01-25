import re
from typing import Dict, List, Match, Optional, Tuple


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


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        blocks: List[str] = fp.read().split("\n\n")

    workflows_str: List[str] = blocks[0].splitlines()
    parts_str: List[str] = blocks[1].splitlines()

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

    parts: Dict[int, Dict[str, int]] = {}
    prop_regex: str = r"(\w)=(\d+)"

    # parse parts
    for part_number, line in enumerate(parts_str):
        attributes: List[str] = line[1:-1].split(",")
        parts[part_number] = {}

        for attribute in attributes:
            matches = re.search(prop_regex, attribute)

            assert matches is not None
            attr = matches.group(1)
            value = int(matches.group(2))
            parts[part_number][attr] = value

    accepted_parts = []

    # apply rules to all parts
    for part_number, part in parts.items():
        wf: str = "in"

        while True:
            if wf == "R":
                break
            if wf == "A":
                accepted_parts.append(part_number)
                break

            for rule_ in workflows[wf].rules:
                attr, comp, value, _ = rule_.values()
                if comp == "<":
                    if part[attr] < value:
                        wf = rule_.workflow
                        break
                else:
                    if part[attr] > value:
                        wf = rule_.workflow
                        break
            else:
                wf = workflows[wf].final

    # calculate sum of attributes
    total_sum: int = 0
    for part_number in accepted_parts:
        for k, v in parts[part_number].items():
            total_sum += v

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 19114
    print(solution("./input.txt"))  # 398527
