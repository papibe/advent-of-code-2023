package main

import (
	"fmt"
	"os"
	"strings"
)

func solution(filename string) int {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(raw_data), "\n")
	data := strings.Split(content, "\n")

	platform := [][]rune{}
	for _, line := range data {
		row := []rune{}
		for _, char := range line {
			row = append(row, char)
		}
		platform = append(platform, row)
	}

	// tilt
	for row := 1; row < len(platform); row++ {
		for col := 0; col < len(platform[0]); col++ {
			item := platform[row][col]
			if item == 'O' {
				// rock_row := row
				for rock_row := row - 1; rock_row >= 0; rock_row-- {
					if platform[rock_row][col] == 'O' || platform[rock_row][col] == '#' {
						break
					}
					platform[rock_row][col], platform[rock_row+1][col] = platform[rock_row+1][col], platform[rock_row][col]
				}
			}
		}
	}

	total_load := 0
	for row := 0; row < len(platform); row++ {
		for col := 0; col < len(platform[0]); col++ {
			if platform[row][col] == 'O' {
				total_load += len(platform) - row
			}
		}
	}

	return total_load
}

func main() {
	fmt.Println(solution("./example.txt")) // 136
	fmt.Println(solution("./input.txt"))   // 110090
}
