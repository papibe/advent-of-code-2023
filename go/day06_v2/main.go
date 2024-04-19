package main

import (
	"fmt"
	"math"
)

func solution(race_stats [][]int) int {
	multiplication := 1

	for _, item := range race_stats {
		time, distance := item[0], item[1]

		square := math.Sqrt(math.Pow(float64(time), 2) - 4*float64(distance))
		x1 := (float64(time) - square) / 2
		x2 := (float64(time) + square) / 2

		_, fraction := math.Modf(x1)
		if fraction == 0 {
			x1 += 1
		}
		_, fraction = math.Modf(x2)
		if fraction == 0 {
			x2 -= 1
		}

		multiplication *= int(math.Floor(x2)-math.Ceil(x1)) + 1
	}
	return multiplication
}

func main() {
	fmt.Println("Part 1")
	example := [][]int{{7, 9}, {15, 40}, {30, 200}}
	input := [][]int{{54, 302}, {94, 1476}, {65, 1029}, {92, 1404}}
	fmt.Println("example: ", solution(example)) // 288
	fmt.Println("intput:  ", solution(input))   // 1195150
	fmt.Println()

	fmt.Println("Part 2")
	example = [][]int{{71530, 940200}}
	input = [][]int{{54946592, 302147610291404}}
	fmt.Println("example: ", solution(example)) // 71503
	fmt.Println("intput:  ", solution(input))   // 42550411
}
