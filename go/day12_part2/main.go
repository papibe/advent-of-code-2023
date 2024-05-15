package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Tuple struct {
	current_size int
	index        int
	nindex       int
}

func check(spring string, numbers []int) int {
	memo := make(map[Tuple]int)

	var _check func(current_size, index, nindex int) int

	_check = func(current_size, index, nindex int) int {
		key := Tuple{current_size, index, nindex}
		value, is_in_memo := memo[key]
		if is_in_memo {
			return value
		}

		// border condition
		if index == len(spring) {
			if nindex == len(numbers) {
				return 1
			} else {
				return 0
			}
		}

		result := 0
		if spring[index] == '#' {
			result += _check(current_size+1, index+1, nindex)

		} else if spring[index] == '.' && current_size > 0 && nindex < len(numbers) && current_size == numbers[nindex] {
			result += _check(0, index+1, nindex+1)

		} else if spring[index] == '.' && current_size == 0 {
			result += _check(0, index+1, nindex)

		} else if spring[index] == '?' {

			// chose '#'
			result += _check(current_size+1, index+1, nindex)

			// chose '.'
			if current_size > 0 && nindex < len(numbers) && current_size == numbers[nindex] {
				result += _check(0, index+1, nindex+1)

			} else if current_size == 0 {
				result += _check(0, index+1, nindex)

			}
		}
		memo[key] = result
		return result
	}

	return _check(0, 0, 0)
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")

	total_sum := 0
	for _, line := range lines {
		sp_line := strings.Split(line, " ")
		springs, numbers_str := sp_line[0], sp_line[1]

		numbers := []int{}
		for _, n_str := range strings.Split(numbers_str, ",") {
			number, _ := strconv.Atoi(n_str)
			numbers = append(numbers, number)
		}

		new_numbers := []int{}
		for i := 0; i < 5; i++ {
			new_numbers = append(new_numbers, numbers...)
		}

		new_springs := []string{}
		for i := 0; i < 5; i++ {
			new_springs = append(new_springs, springs)
		}

		final_springs := strings.Join(new_springs, "?") + "."

		total_sum += check(final_springs, new_numbers)

	}
	return total_sum
}

func main() {
	fmt.Println(solution("./example.txt")) // 525152
	fmt.Println(solution("./input.txt"))   // 65607131946466
}
