package main

import (
	"fmt"
	"os"
	"regexp"
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

	directions := lines[0]
	re := regexp.MustCompile(`(\w+) = \((\w+), (\w+)\)`)

	network := make(Network)

	for _, line := range lines[2:] {
		matches := re.FindStringSubmatch(line)
		// value := map[string]string{"L": matmatches[2], "R": matmatches[3]}
		network[matches[1]] = map[rune]string{'L': matches[2], 'R': matches[3]}
	}

	starting_positions := []string{}
	for position, _ := range network {
		if position[len(position)-1] == 'A' {
			starting_positions = append(starting_positions, position)
		}
	}

	path_info := []map[string]int{}
	for _, position := range starting_positions {
		seen := make(map[string]int)
		index := 0
		counter := 0
		seen[position] = counter

		for {
			position = network[position][rune(directions[index])]
			index = (index + 1) % len(directions)
			counter += 1

			_, already_seen := seen[position]
			if already_seen && position[len(position)-1] == 'Z' {
				path_info = append(path_info, map[string]int{
					"prefix": seen[position],
					"cycle":  counter - seen[position],
				})
				break
			} else {
				seen[position] = counter
			}
		}

	}

	current_lcm := 1
	for _, cycle := range path_info {
		current_lcm = LCM(current_lcm, cycle["cycle"])
	}

	return current_lcm
}

func main() {
	fmt.Println(solution("./example3.txt")) // 6
	fmt.Println(solution("./input.txt"))    // 12357789728873
}
