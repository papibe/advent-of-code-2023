import re

CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
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

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIRS = 3
ONE_PAIR = 2
HIGH_CARD = 1


def hand_type(hand: str) -> int:
    freq = {}
    for card in hand:
        freq[card] = freq.get(card, 0) + 1

    repeats = sorted(freq.values(), reverse=True)

    if repeats[0] == 5:
        return FIVE_OF_A_KIND
    if repeats[0] == 4:
        return FOUR_OF_A_KIND
    if repeats[0] == 3 and repeats[1] == 2:
        return FULL_HOUSE
    if repeats[0] == 3:
        return THREE_OF_A_KIND
    if repeats[0] == 2 and repeats[1] == 2:
        return TWO_PAIRS
    if repeats[0] == 2:
        return ONE_PAIR

    return HIGH_CARD


def compare_cards(hand):
    list_of_values = [hand[0]]
    for card in hand[1]:
        list_of_values.append(CARD_VALUES[card])
    return list_of_values


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    list_of_cards = []
    for line in data:
        hand, bet = line.split(" ")
        list_of_cards.append([hand_type(hand), hand, int(bet)])

    ranked_hands = sorted(list_of_cards, key=compare_cards)

    total_winnings = 0
    index = 0
    for _, _, bet in ranked_hands:
        index += 1
        total_winnings += index * bet

    return total_winnings


if __name__ == "__main__":
    print(solution("./example.txt"))  # 6440
    print(solution("./input.txt"))  # 251545216
