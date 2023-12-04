import re
from collections import deque


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    line_regex = r"Card\s+(\d+): ([^|]*) \| ([^|]*)"
    num_regex = r"\d+"

    # scratchcards_points = {}
    scratchcards_count = {}

    for line in data:
        match = re.search(line_regex, line)
        card_number = int(match.group(1))

        wining = {n for n in re.findall(num_regex, match.group(2))}

        points = 0
        for my_card in re.findall(num_regex, match.group(3)):
            if my_card in wining:
                points += 1

        scratchcards_count[card_number] = scratchcards_count.get(card_number, 0) + 1

        for gained_card in range(card_number + 1, card_number + 1 + points):
            scratchcards_count[gained_card] = (
                scratchcards_count.get(gained_card, 0) + scratchcards_count[card_number]
            )

    return sum(scratchcards_count.values())


if __name__ == "__main__":
    print(solution("./example.txt"))  # 30
    print(solution("./input.txt"))  # 5489600
