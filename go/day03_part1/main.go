package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Coord struct {
	row int
	col int
}

var STEPS = []Coord{
	{-1, -1},
	{-1, 0},
	{-1, 1},
	{0, -1},
	{0, 1},
	{1, -1},
	{1, 0},
	{1, 1},
}

func isNumeric(c byte) bool {
	return c >= '0' && c <= '9'
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")

	total_sum := 0

	for row := 0; row < len(lines); row++ {
		line := lines[row]

		index := 0
		for index < len(line) {
			start := index
			for index < len(line) && isNumeric(line[index]) {
				index += 1
			}

			if isNumeric(line[start]) && isNumeric(line[index-1]) {

				near_symbol := false
			outer:
				for col := start; col < index; col++ {
					for _, step := range STEPS {
						new_row := row + step.row
						new_col := col + step.col

						if new_row >= 0 && new_row < len(lines) && new_col >= 0 && new_col < len(line) {
							if !isNumeric(lines[new_row][new_col]) && lines[new_row][new_col] != '.' {
								near_symbol = true
								break outer
							}
						}
					}
				}
				if near_symbol {
					local_sum, _ := strconv.Atoi(string(line[start:index]))
					total_sum += local_sum
				}
			}
			index += 1
		}
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 4361
	fmt.Println(solution("./input.txt"))   // 519444
}
