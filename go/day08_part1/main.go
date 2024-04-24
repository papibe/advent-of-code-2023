package main

import (
	"fmt"
	"os"
	"regexp"
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

	directions := lines[0]
	re := regexp.MustCompile(`(\w+) = \((\w+), (\w+)\)`)

	network := make(Network)

	for _, line := range lines[2:] {
		matches := re.FindStringSubmatch(line)
		// value := map[string]string{"L": matmatches[2], "R": matmatches[3]}
		network[matches[1]] = map[rune]string{'L': matches[2], 'R': matches[3]}
	}

	position := "AAA"
	index := 0
	counter := 0

	for position != "ZZZ" {
		position = network[position][rune(directions[index])]
		index = (index + 1) % len(directions)
		counter += 1
	}

	return counter
}

func main() {
	fmt.Println(solution("./example1.txt")) // 2
	fmt.Println(solution("./example2.txt")) // 6
	fmt.Println(solution("./input.txt"))    // 24253
}
