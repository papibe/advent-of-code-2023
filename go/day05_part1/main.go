package main

import (
	"fmt"
	"math"
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
	re := regexp.MustCompile(`\d+`)

	content := strings.Trim(string(data), "\n")
	blocks := strings.Split(content, "\n\n")
	seeds := []int{}
	first_line := strings.Split(strings.Trim(blocks[0], "\n"), "\n")[0]
	for _, str_n := range re.FindAllString(first_line, -1) {
		n, _ := strconv.Atoi(str_n)
		seeds = append(seeds, n)
	}

	almanac := make(map[int][]map[string]int)

	for map_number, block := range blocks[1:] {
		list_of_ranges := []map[string]int{}
		for _, line := range strings.Split(strings.Trim(block, "\n"), "\n")[1:] {
			numbers := []int{}
			first_line = strings.Split(strings.Trim(line, "\n"), "\n")[0]
			for _, str_n := range re.FindAllString(first_line, -1) {
				n, _ := strconv.Atoi(str_n)
				numbers = append(numbers, n)
			}

			d := map[string]int{
				"start": numbers[1],
				"len_":  numbers[2],
				"end":   numbers[1] + numbers[2] - 1,
				"trans": numbers[0],
			}
			list_of_ranges = append(list_of_ranges, d)
		}
		almanac[map_number] = list_of_ranges
	}

	min_location := math.MaxInt
	for _, seed := range seeds {
		for index := 0; index < len(almanac); index++ {
			lor := almanac[index]
			for _, d := range lor {
				if d["start"] <= seed && seed <= d["end"] {
					seed = d["trans"] + seed - d["start"]
					break
				}
			}
		}
		min_location = min(min_location, seed)
	}
	return min_location
}

func main() {
	fmt.Println(solution("./example.txt")) // 35
	fmt.Println(solution("./input.txt"))   // 3374647
}
