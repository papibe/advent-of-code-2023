package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Edge struct {
	row int
	col int
}

var STEPS = map[rune][2]int{
	'0': {0, 1},
	'2': {0, -1},
	'3': {-1, 0},
	'1': {1, 0},
}

func abs(a int) int {
	if a > 0 {
		return a
	}
	return -a
}

// references
// https://en.wikipedia.org/wiki/Shoelace_formula
// https://en.wikipedia.org/wiki/Pick%27s_theorem

func solution(filename string) int {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(raw_data), "\n")
	data := strings.Split(content, "\n")

	re := regexp.MustCompile(`(\w+) (\w+) \(#(\w+)\)`)

	row, col := 0, 0
	edges := []Edge{{row, col}}

	boundary := 0

	for _, line := range data {
		matches := re.FindStringSubmatch(line)

		hex_digits := matches[3]
		u_amount, _ := strconv.ParseUint(hex_digits[:5], 16, 40)
		amount := int(u_amount)
		direction := rune(hex_digits[len(hex_digits)-1])

		boundary += amount

		next_row := row + STEPS[direction][0]*amount
		next_col := col + STEPS[direction][1]*amount

		edges = append(edges, Edge{next_row, next_col})
		row, col = next_row, next_col
	}

	area := 0
	for i := 0; i < len(edges)-1; i++ {
		area += (edges[i].col + edges[i+1].col) * (edges[i].row - edges[i+1].row)
	}

	return (abs(area/2) - (boundary / 2) + 1) + boundary
}

func main() {
	fmt.Println(solution("./example.txt")) // 952408144115
	fmt.Println(solution("./input.txt"))   // 60612092439765
}
