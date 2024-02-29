package main

import (
	"fmt"
	"os"
	"strings"
)

var DIGITS = map[rune]bool{
	'1': true,
	'2': true,
	'3': true,
	'4': true,
	'5': true,
	'6': true,
	'7': true,
	'8': true,
	'9': true,
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")

	var min_index int
	var max_index int
	addition := 0
	for _, line := range strings.Split(content, "\n") {
		// get first digit's index
		for i := 0; i < len(line); i++ {
			_, is_digit := DIGITS[rune(line[i])]
			if is_digit {
				min_index = i
				break
			}
		}
		// get last digit's index
		for i := len(line) - 1; i >= 0; i-- {
			_, is_digit := DIGITS[rune(line[i])]
			if is_digit {
				max_index = i
				break
			}
		}
		// adding calibration value (composed from first and last digits)
		addition += int(line[min_index]-'0')*10 + int(line[max_index]-'0')
	}
	return addition
}

func main() {
	fmt.Println(solution("./example.txt")) // 142
	fmt.Println(solution("./input.txt"))   // 54667
}
