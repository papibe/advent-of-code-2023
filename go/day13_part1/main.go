package main

import (
	"fmt"
	"os"
	"strings"
)

func get_vertical_reflection(pattern []string) int {

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
		if found {
			return col + 1
		}
	}
	return 0
}

func get_horizontal_reflection(pattern []string) int {

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
		if found {
			return row + 1
		}
	}
	return 0
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	patterns := strings.Split(content, "\n\n")

	total_sum := 0
	for _, raw_pattern := range patterns {

		pattern := strings.Split(raw_pattern, "\n")
		col := get_vertical_reflection(pattern)
		total_sum += col

		row := get_horizontal_reflection(pattern)
		total_sum += row * 100
		// fmt.Println(pattern)
		// fmt.Println(row, col)
	}
	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 405
	fmt.Println(solution("./input.txt"))   // 33122
}
