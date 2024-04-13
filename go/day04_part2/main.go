package main

import (
	"fmt"
	"os"
	"regexp"
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

	scratchcards_points := make(map[int]int)

	for count, line := range lines {
		counter := count + 1
		matches := line_re.FindStringSubmatch(line)
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
		scratchcards_points[counter] = points

	}
	// BFS like cycle
	queue := []int{}
	processed_cards := 0

	for card := range scratchcards_points {
		queue = append(queue, card)
	}

	// main BFS
	for len(queue) > 0 {
		card := queue[0]
		queue = queue[1:]
		processed_cards += 1
		for gained_card := card + 1; gained_card < card+1+scratchcards_points[card]; gained_card++ {
			queue = append(queue, gained_card)
		}
	}

	return processed_cards
}

func main() {
	fmt.Println(solution("./example.txt")) // 30
	fmt.Println(solution("./input.txt"))   // 5489600
}
