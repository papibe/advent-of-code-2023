package main

import (
	"fmt"
	"os"
	"strings"
)

func cycle(platform [][]rune) {

	// north tilt
	for row := 1; row < len(platform); row++ {
		for col := 0; col < len(platform[0]); col++ {
			if platform[row][col] == 'O' {
				for rock_row := row - 1; rock_row >= 0; rock_row-- {
					if platform[rock_row][col] == 'O' || platform[rock_row][col] == '#' {
						break
					}
					platform[rock_row][col], platform[rock_row+1][col] = platform[rock_row+1][col], platform[rock_row][col]
				}
			}
		}
	}

	// west tilt
	for col := 1; col < len(platform[0]); col++ {
		for row := 0; row < len(platform); row++ {
			if platform[row][col] == 'O' {
				for rock_col := col - 1; rock_col >= 0; rock_col-- {
					if platform[row][rock_col] == 'O' || platform[row][rock_col] == '#' {
						break
					}
					platform[row][rock_col], platform[row][rock_col+1] = platform[row][rock_col+1], platform[row][rock_col]
				}
			}
		}
	}

	// south tilt
	for row := len(platform) - 2; row >= 0; row-- {
		for col := 0; col < len(platform[0]); col++ {
			if platform[row][col] == 'O' {
				for rock_row := row + 1; rock_row < len(platform); rock_row++ {
					if platform[rock_row][col] == 'O' || platform[rock_row][col] == '#' {
						break
					}
					platform[rock_row][col], platform[rock_row-1][col] = platform[rock_row-1][col], platform[rock_row][col]
				}
			}
		}
	}

	// east tilt
	for col := len(platform[0]) - 2; col >= 0; col-- {
		for row := 0; row < len(platform); row++ {
			if platform[row][col] == 'O' {
				for rock_col := col + 1; rock_col < len(platform[0]); rock_col++ {
					if platform[row][rock_col] == 'O' || platform[row][rock_col] == '#' {
						break
					}
					platform[row][rock_col], platform[row][rock_col-1] = platform[row][rock_col-1], platform[row][rock_col]
				}
			}
		}
	}

}

func hash(platform [][]rune) string {
	concat_string := []string{}
	for _, row := range platform {
		concat_string = append(concat_string, string(row))
	}
	return strings.Join(concat_string, "")
}

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

	goal := 1000000000
	seen := make(map[string]int)
	start_key := ""
	start_index := 0
	for index := 0; index < goal; index++ {
		key := hash(platform)
		_, has_been_seen := seen[key]
		if has_been_seen {
			start_key = key
			start_index = index
			break
		}
		seen[key] = index
		cycle(platform)
	}

	prefix := seen[start_key]
	rock_cycle := start_index - prefix
	actual_cycle := (goal - prefix) % rock_cycle

	for i := 0; i < actual_cycle; i++ {
		cycle(platform)
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
	fmt.Println(solution("./example.txt")) // 64
	fmt.Println(solution("./input.txt"))   // 95254
}
