package main

import (
	"fmt"
)

func solution(race_stats [][]int) int {
	multiplication := 1

	for _, item := range race_stats {
		time, distance := item[0], item[1]
		counter := 0
		for hold := 0; hold <= time; hold++ {
			speed := hold
			my_distance := (time - hold) * speed
			if my_distance > distance {
				counter += 1
			}
		}
		multiplication *= counter
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
