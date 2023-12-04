import re
from collections import deque


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    line_regex = r"Card\s+(\d+): ([^|]*) \| ([^|]*)"
    num_regex = r"\d+"

    scratchcards_points = {}
    counter = 0

    for line in data:
        counter += 1

        match = re.search(line_regex, line)
        wining = {n for n in re.findall(num_regex, match.group(2))}

        points = 0
        for my_card in re.findall(num_regex, match.group(3)):
            if my_card in wining:
                points += 1

        scratchcards_points[counter] = points

    # BFS like cycle
    queue = deque()
    processed_cards = 0

    # push all cards to queue
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
