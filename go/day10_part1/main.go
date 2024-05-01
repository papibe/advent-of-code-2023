package main

import (
	"fmt"
	"os"
	"strings"
)

type Tuple struct {
	row int
	col int
}

type Deque [][3]int
type VisitedSet map[Tuple]bool

func (q *Deque) popleft() (int, int, int) {
	item := (*q)[0]
	(*q) = (*q)[1:]
	return item[0], item[1], item[2]
}

func (v VisitedSet) add(t Tuple) {
	v[t] = true
}

const START = 'S'

var landscape = map[rune][][]int{
	'|': {{1, 0}, {-1, 0}},
	'-': {{0, -1}, {0, 1}},
	'L': {{-1, 0}, {0, 1}},
	'J': {{-1, 0}, {0, -1}},
	'7': {{0, -1}, {1, 0}},
	'F': {{1, 0}, {0, 1}},
	'.': {},
	'S': {{1, 0}, {-1, 0}},
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	lines := strings.Split(content, "\n")

	start_row := -1
	start_col := -1

outer_loop:
	for row, line := range lines {
		for col, char := range line {
			if char == START {
				start_row = row
				start_col = col
				break outer_loop
			}
		}
	}

	queue := Deque{{start_row, start_col, 0}}
	visited := make(VisitedSet)
	visited[Tuple{start_row, start_col}] = true

	for len(queue) > 0 {
		row, col, steps := queue.popleft()

		for _, item := range landscape[rune(lines[row][col])] {
			new_row := row + item[0]
			new_col := col + item[1]
			if 0 <= new_row && new_row < len(lines) && 0 <= new_col && new_col < len(lines[0]) {
				key := Tuple{new_row, new_col}
				_, is_visited := visited[key]
				if lines[new_row][new_col] != '.' && !is_visited {
					queue = append(queue, [3]int{new_row, new_col, steps + 1})
					visited.add(key)
				}
			}
		}
	}

	return len(visited) / 2
}

func main() {
	fmt.Println(solution("./example1.txt")) // 4
	fmt.Println(solution("./example2.txt")) // 8
	fmt.Println(solution("./input.txt"))    // 6701
}
