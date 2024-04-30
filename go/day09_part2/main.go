package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Network map[string]map[rune]string

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")

	sequences := [][]int{}
	for _, line := range lines {
		sequence := []int{}
		for _, str_int := range strings.Split(line, " ") {
			integer, _ := strconv.Atoi(str_int)
			sequence = append(sequence, integer)
		}
		sequences = append(sequences, sequence)
	}

	total_sum := 0

	for _, sequence := range sequences {
		triangle := [][]int{sequence}

		prev_row := triangle[len(triangle)-1]
		condition := false
		for _, n := range prev_row {
			condition = condition || (n != 0)
		}

		for condition {
			next_row := []int{}
			for i := 0; i < len(prev_row)-1; i++ {
				next_row = append(next_row, 0)
			}

			for i := 0; i < len(prev_row)-1; i++ {
				next_row[i] = prev_row[i+1] - prev_row[i]
			}

			triangle = append(triangle, next_row)
			prev_row = triangle[len(triangle)-1]

			condition = false
			for _, n := range prev_row {
				condition = condition || (n != 0)
			}
		}

		n := len(triangle) - 1
		triangle[n] = append([]int{0}, triangle[n]...)
		for i := len(triangle) - 2; i >= 0; i-- {
			triangle[i] = append([]int{triangle[i][0] - triangle[i+1][0]}, triangle[i]...)
		}

		total_sum += triangle[0][0]
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 2
	fmt.Println(solution("./input.txt"))   // 1089
}
