package main

import (
	"fmt"
	"os"
	"strings"
)

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")
	line := lines[0]

	total_sum := 0
	for _, sequence := range strings.Split(line, ",") {
		ascii_value := 0
		for _, char := range sequence {
			ascii_value += int(char)
			ascii_value *= 17
			ascii_value %= 256
		}
		total_sum += ascii_value
	}
	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 1320
	fmt.Println(solution("./input.txt"))   // 516070
}
