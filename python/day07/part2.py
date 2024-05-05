from typing import Dict, List, Tuple

comparing_hand = Tuple[List[int], str, int]
ranked_hand = Tuple[List[int], int, int, int, int, int]

CARD_VALUES: Dict[str, int] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

JOKER: str = "J"


def hand_type(hand: str) -> List[int]:
    freq: Dict[str, int] = {}
    jokers: int = 0
    for card in hand:
        if card == JOKER:
            jokers += 1
        else:
            freq[card] = freq.get(card, 0) + 1

    repeats = sorted(freq.values(), reverse=True)

    # JJJJJ => repeats will be empty
    if not repeats:
        return [jokers]

    repeats[0] += jokers

    return repeats


def compare_cards(hand: comparing_hand) -> List[int]:
    list_of_values: List[int] = []
    for card in hand[1]:
        list_of_values.append(CARD_VALUES[card])
    return [*hand[0], *list_of_values]


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    list_of_cards: List[comparing_hand] = []
    for line in data:
        hand, bet = line.split(" ")
        list_of_cards.append((hand_type(hand), hand, int(bet)))

    ranked_hands: List[comparing_hand] = sorted(list_of_cards, key=compare_cards)

    total_winnings: int = 0
    index: int = 0
    for _, _, bet_ in ranked_hands:
        index += 1
        total_winnings += index * bet_

    return total_winnings


if __name__ == "__main__":
    print(solution("./example.txt"))  # 5905
    print(solution("./input.txt"))  # 250384185
