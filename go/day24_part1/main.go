package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type Hailstone struct {
	x  int
	y  int
	z  int
	dx int
	dy int
	dz int
}

func solution(filename string, lower, high int) int {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(raw_data), "\n")
	data := strings.Split(content, "\n")

	hailstones := []Hailstone{}
	for _, line := range data {
		parts := strings.Split(line, " @ ")
		positions := strings.Split(parts[0], ", ")
		velocities := strings.Split(parts[1], ", ")
		x, _ := strconv.Atoi(strings.Trim(positions[0], " "))
		y, _ := strconv.Atoi(strings.Trim(positions[1], " "))
		z, _ := strconv.Atoi(strings.Trim(positions[2], " "))

		dx, _ := strconv.Atoi(strings.Trim(velocities[0], " "))
		dy, _ := strconv.Atoi(strings.Trim(velocities[1], " "))
		dz, _ := strconv.Atoi(strings.Trim(velocities[2], " "))

		hailstones = append(hailstones, Hailstone{x, y, z, dx, dy, dz})
	}

	// fmt.Println(hailstones)

	number_of_hailstones := len(hailstones)
	interserctions := 0

	for i := 0; i < number_of_hailstones; i++ {
		for j := i + 1; j < number_of_hailstones; j++ {

			// use y = m*x + c  form to represent a line in xy plane:
			// first line (i) ya = dxa*x + xa
			// second line (j) yb = dxb*x + xb
			ma := float64(hailstones[i].dy) / float64(hailstones[i].dx)
			mb := float64(hailstones[j].dy) / float64(hailstones[j].dx)
			ca := float64(hailstones[i].y) - ma*float64(hailstones[i].x)
			cb := float64(hailstones[j].y) - mb*float64(hailstones[j].x)

			if math.Abs(float64(ma)-float64(mb)) < 0.0000001 {
				continue
			}

			var xi = (cb - ca) / (ma - mb)
			var yi = (xi * ma) + ca

			x_is_in_range := float64(lower) <= xi && xi <= float64(high)
			y_is_in_range := float64(lower) <= yi && yi <= float64(high)
			xi_is_in_the_future_of_i := (xi > float64(hailstones[i].x)) == (float64(hailstones[i].x)+float64(hailstones[i].dx) > float64(hailstones[i].x))
			xi_is_in_the_future_of_j := (xi > float64(hailstones[j].x)) == (float64(hailstones[j].x)+float64(hailstones[j].dx) > float64(hailstones[j].x))

			if x_is_in_range && y_is_in_range && xi_is_in_the_future_of_i && xi_is_in_the_future_of_j {
				interserctions += 1
			}
		}
	}

	return interserctions
}

func main() {
	fmt.Println(solution("./example.txt", 7, 27))                          // 2
	fmt.Println(solution("./input.txt", 200000000000000, 400000000000000)) // 13910
}
