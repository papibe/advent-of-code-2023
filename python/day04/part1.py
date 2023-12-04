import re


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    line_regex = r"Card\s+\d+: ([^|]*) \| ([^|]*)"
    num_regex = r"\d+"
    total_points = 0

    for line in data:
        match = re.search(line_regex, line)
        wining = {n for n in re.findall(num_regex, match.group(1))}

        points = 0
        for my_card in re.findall(num_regex, match.group(2)):
            if my_card in wining:
                if points == 0:
                    points = 1
                else:
                    points *= 2

        total_points += points

    return total_points


if __name__ == "__main__":
    print(solution("./example.txt"))  # 13
    print(solution("./input.txt"))  # 20855
