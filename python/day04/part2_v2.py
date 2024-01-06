import re
from typing import Dict, List, Set


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    line_regex: str = r"Card\s+(\d+): ([^|]*) \| ([^|]*)"
    num_regex: str = r"\d+"

    scratchcards_count: Dict[int, int] = {}

    for line in data:
        matches = re.search(line_regex, line)
        assert matches is not None
        card_number = int(matches.group(1))

        wining: Set[int] = {n for n in re.findall(num_regex, matches.group(2))}

        points: int = 0
        for my_card in re.findall(num_regex, matches.group(3)):
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
