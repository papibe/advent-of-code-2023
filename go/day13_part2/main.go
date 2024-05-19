package main

import (
	"fmt"
	"os"
	"strings"
)

const NONE = -1

var CHANGE = map[rune]rune{
	'#': '.',
	'.': '#',
}

func parse(filename string) [][][]rune {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	patterns := strings.Split(content, "\n\n")

	all_patterns := [][][]rune{}
	for _, raw_pattern := range patterns {
		pattern := [][]rune{}
		for _, line := range strings.Split(raw_pattern, "\n") {

			row := []rune(line)
			pattern = append(pattern, row)
		}
		all_patterns = append(all_patterns, pattern)
	}

	return all_patterns
}

func get_vertical_reflection(pattern [][]rune, old_col int) (int, bool) {

	for col := 0; col < len(pattern[0])-1; col++ {
		left := col
		right := col + 1
		found := true

	outer_loop:
		for left >= 0 && right < len(pattern[0]) {
			for row := 0; row < len(pattern); row++ {
				if pattern[row][left] != pattern[row][right] {
					found = false
					break outer_loop
				}
			}
			left--
			right++
		}
		if found && col != old_col {
			return col, true
		}
	}
	return -1, false
}

func get_horizontal_reflection(pattern [][]rune, old_row int) (int, bool) {

	for row := 0; row < len(pattern)-1; row++ {
		up := row
		down := row + 1
		found := true

	outer_loop:
		for up >= 0 && down < len(pattern) {
			for col := 0; col < len(pattern[0]); col++ {
				if pattern[up][col] != pattern[down][col] {
					found = false
					break outer_loop
				}
			}
			up--
			down++
		}
		if found && row != old_row {
			return row, true
		}
	}
	return -1, false
}

func solution(filename string) int {
	patterns := parse(filename)
	total_sum := 0

	for _, pattern := range patterns {

		col, is_vertical_reflection := get_vertical_reflection(pattern, NONE)

		if is_vertical_reflection {
			found := false
			for i, line := range pattern {
				for j, cell := range line {

					if found {
						continue
					}
					pattern[i][j] = CHANGE[cell]

					new_row, new_v_reflection := get_horizontal_reflection(pattern, NONE)
					if new_v_reflection {
						total_sum += (new_row + 1) * 100
						found = true
					}

					new_col, new_h_reflection := get_vertical_reflection(pattern, col)
					if new_h_reflection {
						total_sum += new_col + 1
						found = true
					}

					pattern[i][j] = cell
				}
			}

		}

		row, is_horizontal_reflection := get_horizontal_reflection(pattern, NONE)

		if is_horizontal_reflection {
			found := false
			for i, line := range pattern {
				for j, cell := range line {

					if found {
						continue
					}
					pattern[i][j] = CHANGE[cell]

					new_row, new_v_reflection := get_horizontal_reflection(pattern, row)
					if new_v_reflection {
						total_sum += (new_row + 1) * 100
						found = true
					}

					new_col, new_h_reflection := get_vertical_reflection(pattern, NONE)
					if new_h_reflection {
						total_sum += new_col + 1
						found = true
					}
					pattern[i][j] = cell
				}
			}
		}
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 400
	fmt.Println(solution("./input.txt"))   // 32312
}
