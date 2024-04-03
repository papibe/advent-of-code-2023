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

type Part struct {
	row   int
	start int
	end   int
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

func get_unique_number_id(lines []string, row, col int) Part {
	start := col
	for start >= 0 && isNumeric(lines[row][start]) {
		start -= 1
	}
	if start < 0 {
		start = 0
	} else {
		start += 1
	}
	end := col
	for end < len(lines[row]) && isNumeric(lines[row][end]) {
		end += 1
	}
	return Part{row, start, end}
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

		for index := 0; index < len(line); index++ {
			if line[index] != '*' {
				continue
			}

			parts := make(map[Part]bool)
			for _, step := range STEPS {
				new_row := row + step.row
				new_col := index + step.col

				if new_row >= 0 && new_row < len(lines) && new_col >= 0 && new_col < len(line) {
					if isNumeric(lines[new_row][new_col]) {
						part_id := get_unique_number_id(lines, new_row, new_col)
						parts[part_id] = true
					}
				}
			}
			if len(parts) == 2 {
				ratio := 1
				for part, _ := range parts {
					local_sum, _ := strconv.Atoi(string(lines[part.row][part.start:part.end]))
					ratio *= local_sum
				}
				total_sum += ratio
			}
		}
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 467835
	fmt.Println(solution("./input.txt"))   // 74528807
}
