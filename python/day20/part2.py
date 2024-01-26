import re
from collections import deque
from math import lcm
from typing import Deque, Dict, List, Match, Optional, Tuple

OFF: int = 0
ON: int = 1
LOW_PULSE: int = 2
HIGH_PULSE: int = 3

Queue = Deque[Tuple[str, int, str]]


class Module:
    def __init__(self) -> None:
        self.name: str = ""
        self.node_names: List[str] = []
        self.nodes: List[Module] = []

    def update(self, modules: "Modules") -> None:
        nodes = []
        for node_name in self.node_names:
            if node_name in modules:
                nodes.append(modules[node_name])
        self.nodes = nodes

    def set_memory(self, modules: "Modules") -> None:
        pass

    def receive_high_pulse(self, node_from: str) -> None:
        pass

    def receive_low_pulse(self, node_from: str) -> None:
        pass


Modules = Dict[str, Module]


class Broadcaster(Module):
    def __init__(self, nodes: List[str], queue: Queue) -> None:
        self.name: str = "broadcaster"
        self.node_names: List[str] = nodes
        self.low_pulses: int = 0
        self.high_pulses: int = 0
        self.queue: Queue = queue

    def receive_low_pulse(self, node_from: str) -> None:
        self.broadcast()

    def broadcast(self) -> None:
        for node in self.nodes:
            self.low_pulses += 1
            # print(self.name, "-low->", node.name)
            self.queue.append((self.name, LOW_PULSE, node.name))


class Flipflop(Module):
    def __init__(self, name: str, nodes: List[str], queue: Queue) -> None:
        self.name: str = name
        self.node_names: List[str] = nodes
        self.state: int = OFF
        self.low_pulses: int = 0
        self.high_pulses: int = 0
        self.queue: Queue = queue

    def receive_low_pulse(self, node_from: str) -> None:
        self.state = ON if self.state == OFF else OFF
        sending_pulse: int
        if self.state == ON:
            sending_pulse = HIGH_PULSE
            # msg: str = "-high-"
        else:
            sending_pulse = LOW_PULSE
            # msg: str = "-low-"

        for node in self.nodes:
            self.high_pulses += 1
            # print(self.name, msg, node.name)
            self.queue.append((self.name, sending_pulse, node.name))

    def __repr__(self) -> str:
        return f"t:f {self.name}"


class Conjunction(Module):
    def __init__(self, name: str, nodes: List[str], queue: Queue) -> None:
        self.name: str = name
        self.node_names: List[str] = nodes
        self.low_pulses: int = 0
        self.high_pulses: int = 0
        self.last_pulse: Dict[str, int] = {}
        self.queue: Queue = queue

    def set_memory(self, modules: Modules) -> None:
        # pass
        for node_name, node in modules.items():
            for node_to_name in node.node_names:
                if node_to_name == self.name:
                    self.last_pulse[node_name] = LOW_PULSE
                    break

    def send_pulse(self) -> None:
        sending_pulse = LOW_PULSE
        # msg: str = "-low->"
        for node_name, last_pulse in self.last_pulse.items():
            if last_pulse == LOW_PULSE:
                sending_pulse = HIGH_PULSE
                # msg: str = "-high->"
                break
        for node in self.nodes:
            # print(self.name, msg, node.name)
            self.queue.append((self.name, sending_pulse, node.name))

    def receive_high_pulse(self, node_from: str) -> None:
        self.last_pulse[node_from] = HIGH_PULSE
        self.send_pulse()

    def receive_low_pulse(self, node_from: str) -> None:
        self.last_pulse[node_from] = LOW_PULSE
        self.send_pulse()

    def __repr__(self) -> str:
        return f"t:c {self.name}, {self.node_names}"


class Button:
    def __init__(self, broadcaster: Broadcaster, queue: Queue) -> None:
        self.name: str = "button"
        self.broadcaster: Broadcaster = broadcaster
        self.low_pulses: int = 0
        self.high_pulses: int = 0
        self.queue: Queue = queue

    def press(self) -> None:
        self.low_pulses += 1
        # print(self.name, "-low->", "broadcaster")
        self.queue.append((self.name, LOW_PULSE, "broadcaster"))


class Orphan(Module):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.node_names: List[str] = []
        self.nodes: List[Module] = []

    def update(self, modules: Modules) -> None:
        pass

    def __repr__(self) -> str:
        return f"t:o {self.name}, {self.node_names}"


def parse(filename: str) -> Tuple[Button, Modules, Queue, str]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    regex: str = r"^.(\w+) -> (.+)"
    b_regex: str = r"broadcaster -> (.+)"

    queue: Queue = deque()

    modules: Modules = {}
    for line in data:
        name: str
        nodes: List[str]
        if line.startswith("%"):
            matches: Optional[Match[str]] = re.search(regex, line)

            assert matches is not None
            name = matches.group(1)
            nodes = matches.group(2).split(", ")
            ff: Flipflop = Flipflop(name, nodes, queue)
            modules[name] = ff

        elif line.startswith("&"):
            matches = re.search(regex, line)

            assert matches is not None
            name = matches.group(1)
            nodes = matches.group(2).split(", ")
            cc: Conjunction = Conjunction(name, nodes, queue)
            modules[name] = cc

        else:  # broadcaster
            matches = re.search(b_regex, line)

            assert matches is not None
            # name = match.group(1)
            nodes = matches.group(1).split(", ")
            broadcaster: Broadcaster = Broadcaster(nodes, queue)
            modules["broadcaster"] = broadcaster

    button = Button(broadcaster, queue)

    # look for orphan node (exit node)
    orphan_parent: str = ""
    for module_name, module in modules.items():
        for destination in module.node_names:
            if destination not in modules:
                orphan_parent = module.name
                orphan2: Orphan = Orphan(destination)
                modules[destination] = orphan2
                # print(f"-{destination}-")
                break
        else:
            continue
        break

    for module in modules.values():
        module.update(modules)

    for module in modules.values():
        module.set_memory(modules)

    return button, modules, queue, orphan_parent


def solution(filename: str) -> int:
    button, modules, queue, parent_name = parse(filename)
    parent_module: Conjunction = modules[parent_name]  # type: ignore

    counters = {module_name: 0 for module_name in parent_module.last_pulse.keys()}

    for run in range(1, 5000):

        # print("--- BUTTON PUSH ---")
        button.press()
        while queue:
            from_node, pulse, node_to = queue.popleft()
            if pulse == LOW_PULSE:
                modules[node_to].receive_low_pulse(from_node)
            else:
                modules[node_to].receive_high_pulse(from_node)

            if (
                from_node in counters
                and pulse == HIGH_PULSE
                and counters[from_node] == 0
            ):
                counters[from_node] = run

            if all(counter > 0 for counter in counters.values()):
                break
        else:
            continue
        break

    total_lcm: int = 1
    for counter in counters.values():
        total_lcm = lcm(total_lcm, counter)

    return total_lcm


if __name__ == "__main__":
    print(solution("./input.txt"))  # 250924073918341
