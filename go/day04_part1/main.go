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

	line_re := regexp.MustCompile(`Card\s+\d+: ([^|]*) \| ([^|]*)`)
	num_re := regexp.MustCompile(`\d+`)

	total_points := 0

	for _, line := range lines {
		matches := line_re.FindStringSubmatch(line)
		wining := make(map[string]bool)
		for _, n := range num_re.FindAllString(matches[1], -1) {
			// n, _ := strconv.Atoi(str_num)
			wining[n] = true
		}

		points := 0
		for _, my_card := range num_re.FindAllString(matches[2], -1) {
			_, is_in_winning := wining[my_card]
			if is_in_winning {
				if points == 0 {
					points = 1
				} else {
					points *= 2
				}
			}
		}
		total_points += points

	}
	return total_points
}

func main() {
	fmt.Println(solution("./example.txt")) // 13
	fmt.Println(solution("./input.txt"))   // 20855
}
