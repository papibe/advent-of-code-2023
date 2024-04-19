package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type ComparingHand struct {
	points []int
	hands  string
	bet    int
}

var CARD_VALUES = map[rune]string{
	'A': "14",
	'K': "13",
	'Q': "12",
	'J': "11",
	'T': "10",
	'9': "09",
	'8': "08",
	'7': "07",
	'6': "06",
	'5': "05",
	'4': "04",
	'3': "03",
	'2': "02",
}

func sort_freqs(freqs []int) {
	sort.Slice(freqs, func(i, j int) bool {
		return freqs[i] > freqs[j]
	})
}

func hand_type(hand string) []int {
	freq := make(map[rune]int)
	for _, card := range hand {
		value, already_seen := freq[card]
		if already_seen {
			freq[card] = value + 1
		} else {
			freq[card] = 1
		}
	}
	list_of_freqs := []int{}
	for _, value := range freq {
		list_of_freqs = append(list_of_freqs, value)
	}
	sort_freqs(list_of_freqs)
	return list_of_freqs
}

func str_repr(card ComparingHand) string {
	str := []string{}
	for _, point := range card.points {
		str = append(str, strconv.Itoa(point))
	}
	for _, char := range card.hands {
		str = append(str, CARD_VALUES[char])
	}
	return strings.Join(str, "")
}

func sort_by_hand(cards []ComparingHand) {
	sort.Slice(cards, func(i, j int) bool {
		return str_repr(cards[i]) < str_repr(cards[j])
	})
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")

	list_of_cards := []ComparingHand{}
	for _, line := range strings.Split(content, "\n") {
		split_line := strings.Split(line, " ")
		hand, str_bet := split_line[0], split_line[1]
		bet, _ := strconv.Atoi(str_bet)
		list_of_cards = append(list_of_cards, ComparingHand{hand_type(hand), hand, bet})
	}
	sort_by_hand(list_of_cards)

	total_winnings := 0
	for index, hand := range list_of_cards {
		total_winnings += (index + 1) * hand.bet
	}

	return total_winnings
}

func main() {
	fmt.Println(solution("./example.txt")) // 6440
	fmt.Println(solution("./input.txt"))   // 251545216
}
