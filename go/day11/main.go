package main

import (
	"fmt"
	"os"
	"strings"
)

const SPACE = '.'
const GALAXY = '#'

func abs(a int) int {
	if a >= 0 {
		return a
	}
	return -a
}

func solution(filename string, exapanding_factor int) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")

	galaxies := [][2]int{}
	for row, line := range lines {
		for col, char := range line {
			if char == GALAXY {
				galaxies = append(galaxies, [2]int{row, col})
			}
		}
	}

	expanding_rows := []int{}
	for row, line := range lines {
		expanding_row_found := true
		for _, char := range line {
			if char != SPACE {
				expanding_row_found = false
				break
			}
		}
		if expanding_row_found {
			expanding_rows = append(expanding_rows, row)
		}
	}

	expanding_cols := []int{}
	for col := 0; col < len(lines[0]); col++ {
		expanding_col_found := true
		for row := 0; row < len(lines); row++ {
			if lines[row][col] != SPACE {
				expanding_col_found = false
				break
			}
		}
		if expanding_col_found {
			expanding_cols = append(expanding_cols, col)
		}
	}

	// expand rows
	for len(expanding_rows) > 0 {
		expanding_row := expanding_rows[len(expanding_rows)-1]
		expanding_rows = expanding_rows[:len(expanding_rows)-1]
		for index, item := range galaxies {
			row := item[0]
			if row > expanding_row {
				galaxies[index][0] += exapanding_factor - 1
			}
		}
		for i := 0; i < len(expanding_rows); i++ {
			if expanding_rows[i] > expanding_row {
				expanding_rows[i] += exapanding_factor - 1
			}
		}
	}

	// expand cols
	for len(expanding_cols) > 0 {
		expanding_col := expanding_cols[len(expanding_cols)-1]
		expanding_cols = expanding_cols[:len(expanding_cols)-1]
		for index, item := range galaxies {
			col := item[1]
			if col > expanding_col {
				galaxies[index][1] += exapanding_factor - 1
			}
		}
		for i := 0; i < len(expanding_cols); i++ {
			if expanding_cols[i] > expanding_col {
				expanding_cols[i] += exapanding_factor - 1
			}
		}
	}

	total_sum := 0
	for i := 0; i < len(galaxies); i++ {
		for j := i + 1; j < len(galaxies); j++ {
			total_sum += abs(galaxies[i][0]-galaxies[j][0]) + abs(galaxies[i][1]-galaxies[j][1])
		}
	}
	return total_sum
}

func main() {
	fmt.Println("Part 1:", solution("./input.txt", 2))       // 9734203
	fmt.Println("Part 2:", solution("./input.txt", 1000000)) // 568914596391
}
