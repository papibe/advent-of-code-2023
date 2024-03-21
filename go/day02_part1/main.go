package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var MAX_CUBES = map[string]int{
	"red":   12,
	"green": 13,
	"blue":  14,
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")

	re := regexp.MustCompile(`Game (\d+): (.*)$`)
	game_id_sum := 0

	for _, line := range strings.Split(content, "\n") {
		matches := re.FindStringSubmatch(line)
		game_number, _ := strconv.Atoi(matches[1])
		all_subsets := matches[2]
		pass_max_capacity := false
	outer:
		for _, cube_set := range strings.Split(all_subsets, "; ") {
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
				if games_cubes[color] > MAX_CUBES[color] {
					pass_max_capacity = true
					break outer
				}
			}
		}
		if !pass_max_capacity {
			game_id_sum += game_number
		}
	}
	return game_id_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 8
	fmt.Println(solution("./input.txt"))   // 2156
}
