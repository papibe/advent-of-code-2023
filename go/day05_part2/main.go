package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func proc_range(almanac map[int][]map[string]int, intervals [][]int) [][]int {
	rule_n := 1

	for i := 0; i < len(almanac); i++ {
		lor := almanac[i]
		rule_n += 1
		rule_output := [][]int{}
		for len(intervals) > 0 {
			item := intervals[len(intervals)-1]
			intervals = intervals[:len(intervals)-1]

			a, b := item[0], item[1]
			apply_rule := -1
			flag := true
			for rn, rule_d := range lor {
				c, d := rule_d["start"], rule_d["end"]

				if b < c || d < a {
					continue
				}
				apply_rule = rn

				c, d = lor[apply_rule]["start"], lor[apply_rule]["end"]

				i_s := max(a, c)
				i_e := min(b, d)

				if i_s < i_e {
					t_s := lor[apply_rule]["trans"] + i_s - lor[apply_rule]["start"]
					t_e := lor[apply_rule]["trans"] + i_e - lor[apply_rule]["start"]
					rule_output = append(rule_output, []int{t_s, t_e})

					if i_s > a {
						intervals = append(intervals, []int{a, i_s})
					}
					if b > i_e {
						intervals = append(intervals, []int{i_e, b})
					}
					flag = false
					break
				}
			}
			if flag {
				rule_output = append(rule_output, []int{a, b})
			}
		}
		intervals = rule_output
	}
	return intervals
}

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
				"end":   numbers[1] + numbers[2],
				"trans": numbers[0],
			}
			list_of_ranges = append(list_of_ranges, d)
		}
		almanac[map_number] = list_of_ranges
	}

	seed_intervals := [][]int{}
	for index, seed_start := range seeds {
		if index%2 == 0 {
			seed_intervals = append(seed_intervals, []int{seed_start, seed_start + seeds[index+1]})
		}
	}

	results := [][]int{}
	for _, item := range seed_intervals {
		start, end := item[0], item[1]
		result := proc_range(almanac, [][]int{{start, end}})
		results = append(results, result...)
	}

	min_value := math.MaxInt
	for _, item := range results {
		value, _ := item[0], item[1]
		min_value = min(min_value, value)
	}

	return min_value
}

func main() {
	fmt.Println(solution("./example.txt")) // 46
	fmt.Println(solution("./input.txt"))   // 6082852
}
