package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Network map[string]map[rune]string

// greatest common divisor (GCD) via Euclidean algorithm
func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// find Least Common Multiple (LCM) via GCD
func LCM(a, b int, integers ...int) int {
	result := a * b / GCD(a, b)

	for i := 0; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

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

		triangle[len(triangle)-1] = append(triangle[len(triangle)-1], 0)
		for i := len(triangle) - 2; i >= 0; i-- {
			n := len(triangle[i]) - 1
			m := len(triangle[i+1]) - 1

			triangle[i] = append(triangle[i], triangle[i][n]+triangle[i+1][m])
		}

		total_sum += triangle[0][len(triangle[0])-1]
	}

	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 114
	fmt.Println(solution("./input.txt"))   // 2101499000
}
