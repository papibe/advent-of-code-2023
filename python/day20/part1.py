import re
from collections import deque

OFF = 0
ON = 1
LOW_PULSE = 2
HIGH_PULSE = 3


class Module:
    def update(self, modules):
        nodes = []
        for node_name in self.node_names:
            if node_name in modules:
                nodes.append(modules[node_name])
        self.nodes = nodes

    def set_memory(self, modules):
        pass

    def receive_high_pulse(self, node_from):
        pass

    def receive_low_pulse(self, node_from):
        pass


class Broadcaster(Module):
    def __init__(self, nodes, queue):
        self.name = "broadcaster"
        self.node_names = nodes
        self.low_pulses = 0
        self.high_pulses = 0
        self.queue = queue

    def receive_low_pulse(self, node_from):
        self.broadcast()

    def broadcast(self):
        for node in self.nodes:
            self.low_pulses += 1
            # print(self.name, "-low->", node.name)
            self.queue.append((self.name, LOW_PULSE, node.name))


class Flipflop(Module):
    def __init__(self, name, nodes, queue):
        self.name = name
        self.node_names = nodes
        self.state = OFF
        self.low_pulses = 0
        self.high_pulses = 0
        self.queue = queue

    def receive_low_pulse(self, node_from):
        self.state = ON if self.state == OFF else OFF
        if self.state == ON:
            sending_pulse = HIGH_PULSE
            msg = "-high-"
        else:
            sending_pulse = LOW_PULSE
            msg = "-low-"

        for node in self.nodes:
            self.high_pulses += 1
            # print(self.name, msg, node.name)
            self.queue.append((self.name, sending_pulse, node.name))

    def __repr__(self):
        return f"t:f {self.name}"


class Conjunction(Module):
    def __init__(self, name, nodes, queue):
        self.name = name
        self.node_names = nodes
        self.low_pulses = 0
        self.high_pulses = 0
        self.last_pulse = {}
        self.queue = queue

    def set_memory(self, modules):
        # pass
        for node_name, node in modules.items():
            for node_to_name in node.node_names:
                if node_to_name == self.name:
                    self.last_pulse[node_name] = LOW_PULSE
                    break

    def send_pulse(self):
        sending_pulse = LOW_PULSE
        msg = "-low->"
        for node_name, last_pulse in self.last_pulse.items():
            if last_pulse == LOW_PULSE:
                sending_pulse = HIGH_PULSE
                msg = "-high->"
                break
        for node in self.nodes:
            # print(self.name, msg, node.name)
            self.queue.append((self.name, sending_pulse, node.name))

    def receive_high_pulse(self, node_from):
        self.last_pulse[node_from] = HIGH_PULSE
        self.send_pulse()

    def receive_low_pulse(self, node_from):
        self.last_pulse[node_from] = LOW_PULSE
        self.send_pulse()

    def __repr__(self):
        return f"t:c {self.name}, {self.node_names}"


class Button:
    def __init__(self, broadcaster, queue):
        self.name = "button"
        self.broadcaster = broadcaster
        self.low_pulses = 0
        self.high_pulses = 0
        self.queue = queue

    def press(self):
        self.low_pulses += 1
        # print(self.name, "-low->", "broadcaster")
        self.queue.append((self.name, LOW_PULSE, "broadcaster"))


class Orphan(Module):
    def __init__(self, name):
        self.name = name
        self.node_names = []
        self.nodes = []

    def update(self, modules):
        pass

    def __repr__(self):
        return f"t:o {self.name}, {self.node_names}"


def parse(filename: str):
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    regex = r"^.(\w+) -> (.+)"
    b_regex = r"broadcaster -> (.+)"

    queue = deque()

    modules = {}
    for line in data:
        if line.startswith("%"):
            match = re.search(regex, line)
            name = match.group(1)
            nodes = match.group(2).split(", ")
            ff = Flipflop(name, nodes, queue)
            modules[name] = ff

        elif line.startswith("&"):
            match = re.search(regex, line)
            name = match.group(1)
            nodes = match.group(2).split(", ")
            cc = Conjunction(name, nodes, queue)
            modules[name] = cc

        else:  # broadcaster
            match = re.search(b_regex, line)
            # name = match.group(1)
            nodes = match.group(1).split(", ")
            broadcaster = Broadcaster(nodes, queue)
            modules["broadcaster"] = broadcaster

    button2 = Button(broadcaster, queue)

    # look for orphan node (exit node)
    for module_name, module in modules.items():
        for destination in module.node_names:
            if destination not in modules:
                orphan2 = Orphan(destination)
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

    return button2, modules, queue


def solution(filename: str) -> int:
    button, modules, queue = parse(filename)

    counter_low = 0
    counter_high = 0
    for _ in range(1000):

        # print("--- BUTTON PUSH ---")
        button.press()
        while queue:
            from_node, pulse, node_to = queue.popleft()
            if pulse == LOW_PULSE:
                counter_low += 1
                modules[node_to].receive_low_pulse(from_node)
            else:
                counter_high += 1
                modules[node_to].receive_high_pulse(from_node)

    return counter_low * counter_high


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 32000000
    print(solution("./example2.txt"))  # 11687500
    print(solution("./input.txt"))  # 817896682
