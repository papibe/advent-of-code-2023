import re


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    directions = data[0]
    regex = r"(\w+) = \((\w+), (\w+)\)"

    network = {}

    for line in data[2:]:
        match = re.search(regex, line)
        network[match.group(1)] = {"L": match.group(2), "R": match.group(3)}

    position = "AAA"
    index = 0
    counter = 0

    while position != "ZZZ":
        position = network[position][directions[index]]
        index = (index + 1) % len(directions)
        counter += 1

    return counter


if __name__ == "__main__":
    print(solution("./example1.txt"))  # 2
    print(solution("./example2.txt"))  # 6
    print(solution("./input.txt"))  # 24253
