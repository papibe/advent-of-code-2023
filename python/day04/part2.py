import re
from collections import deque
from typing import Deque, Dict, List, Match, Optional, Set


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    line_regex: str = r"Card\s+(\d+): ([^|]*) \| ([^|]*)"
    num_regex: str = r"\d+"

    scratchcards_points: Dict[int, int] = {}

    for counter, line in enumerate(data):
        counter += 1
        matches: Optional[Match[str]] = re.search(line_regex, line)
        assert matches is not None
        wining: Set[int] = {n for n in re.findall(num_regex, matches.group(2))}

        points: int = 0
        for my_card in re.findall(num_regex, matches.group(3)):
            if my_card in wining:
                points += 1

        scratchcards_points[counter] = points

    # BFS like cycle
    queue: Deque[int] = deque()
    processed_cards: int = 0

    # push all cards to queue
    card: int
    for card in scratchcards_points:
        queue.append(card)

    # main BFS
    while queue:
        card = queue.popleft()
        processed_cards += 1
        for gained_card in range(card + 1, card + 1 + scratchcards_points[card]):
            queue.append(gained_card)

    return processed_cards


if __name__ == "__main__":
    print(solution("./example.txt"))  # 30
    print(solution("./input.txt"))  # 5489600
