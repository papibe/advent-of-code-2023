package main

import (
	"fmt"
	"os"
	"strings"
)

var DIGITS = map[string]int{
	"one":   1,
	"two":   2,
	"three": 3,
	"four":  4,
	"five":  5,
	"six":   6,
	"seven": 7,
	"eight": 8,
	"nine":  9,
}

// func max(a, b int) int {
// 	if a > b {
// 		return a
// 	}
// 	return b
// }

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")

	addition := 0
	for _, line := range strings.Split(content, "\n") {
		numbers := make(map[int]int)

		// check for spelled out digits
		for k, v := range DIGITS {
			index := strings.Index(line, k)

			// check for ALL occurrences of a digit
			for index >= 0 {
				numbers[index] = v
				new_index := strings.Index(line[index+len(k)-1:], k)
				if new_index >= 0 {
					index = index + len(k) - 1 + new_index
				} else {
					index = new_index
				}
			}
		}
		// check for ascii digits
		for index, char := range line {
			if char >= '0' && char <= '9' {
				numbers[index] = int(char) - '0'
			}
		}
		// get first and last indexes
		min_index := len(line)
		max_index := -1
		for index, _ := range numbers {
			max_index = max(max_index, index)
			min_index = min(min_index, index)
		}

		// adding calibration value (composed from first and last digits)
		addition += (numbers[min_index] * 10) + numbers[max_index]
	}
	return addition
}

func main() {
	fmt.Println(solution("./example2.txt")) // 281
	fmt.Println(solution("./input.txt"))    // 54203
}
