package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")

	re := regexp.MustCompile(`Game (\d+): (.*)$`)
	sum_of_powers := 0

	for _, line := range strings.Split(content, "\n") {
		matches := re.FindStringSubmatch(line)
		all_sets := matches[2]

		var max_cubes = map[string]int{
			"red":   0,
			"green": 0,
			"blue":  0,
		}
		power := 1

		for _, cube_set := range strings.Split(all_sets, "; ") {
			cubes := strings.Split(cube_set, ", ")
			games_cubes := make(map[string]int)

			for _, cube := range cubes {
				cube_list := strings.Split(cube, " ")
				number, _ := strconv.Atoi(cube_list[0])
				color := cube_list[1]
				current_value, is_there := games_cubes[color]
				if is_there {
					games_cubes[color] = current_value + number
				} else {
					games_cubes[color] = number
				}

				for color, quantity := range games_cubes {
					max_cubes[color] = max(max_cubes[color], quantity)
				}
				power = 1
				for _, quantity := range max_cubes {
					power *= quantity
				}
			}
		}
		sum_of_powers += power
	}
	return sum_of_powers
}

func main() {
	fmt.Println(solution("./example.txt")) // 2286
	fmt.Println(solution("./input.txt"))   // 66909
}
