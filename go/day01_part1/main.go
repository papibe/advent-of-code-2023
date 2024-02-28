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

	content := string(data)

	addition := 0
	for _, line := range strings.Split(strings.Trim(content, "\n"), "\n") {
		digits := []rune{}
		for _, char := range line {
			if char >= '0' && char <= '9' {
				digits = append(digits, char)
			}
		}
		addition += int(digits[0]-'0')*10 + int(digits[len(digits)-1]-'0')
	}

	return addition
}

func main() {
	fmt.Println(solution("./example.txt")) // 142
	fmt.Println(solution("./input.txt"))   // 54667
}
