package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")

	line_re := regexp.MustCompile(`Card\s+(\d+): ([^|]*) \| ([^|]*)`)
	num_re := regexp.MustCompile(`\d+`)

	scratchcards_count := make(map[int]int)

	for _, line := range lines {
		matches := line_re.FindStringSubmatch(line)
		card_number, _ := strconv.Atoi(matches[1])
		wining := make(map[string]bool)

		for _, n := range num_re.FindAllString(matches[2], -1) {
			wining[n] = true
		}

		points := 0
		for _, my_card := range num_re.FindAllString(matches[3], -1) {
			_, is_in_winning := wining[my_card]
			if is_in_winning {
				points += 1
			}
		}
		_, is_already_there := scratchcards_count[card_number]
		if is_already_there {
			scratchcards_count[card_number] += 1
		} else {
			scratchcards_count[card_number] = 1
		}

		for gained_card := card_number + 1; gained_card < card_number+1+points; gained_card++ {
			_, is_already_there := scratchcards_count[gained_card]
			if is_already_there {
				scratchcards_count[gained_card] += scratchcards_count[card_number]
			} else {
				scratchcards_count[gained_card] = scratchcards_count[card_number]

			}
		}
	}
	processed_cards := 0
	for _, counter := range scratchcards_count {
		processed_cards += counter
	}

	return processed_cards
}

func main() {
	fmt.Println(solution("./example.txt")) // 30
	fmt.Println(solution("./input.txt"))   // 5489600
}
