package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type QueueItem struct {
	row   int
	col   int
	count int
}

type Queue []QueueItem

func (q *Queue) Pop() QueueItem {
	item := (*q)[0]
	*q = (*q)[1:]
	return item
}

func (q *Queue) Push(item QueueItem) {
	(*q) = append((*q), item)
}

func (q Queue) isEmpty() bool {
	return len(q) == 0
}

type Edge struct {
	row int
	col int
}

type Edges map[Edge]bool

func (v Edges) add(item Edge) {
	v[item] = true
}

func (v Edges) contains(e Edge) bool {
	_, ok := v[e]
	return ok
}

var STEPS = map[string][2]int{
	"R": {0, 1},
	"L": {0, -1},
	"U": {-1, 0},
	"D": {1, 0},
}

func solution(filename string) int {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(raw_data), "\n")
	data := strings.Split(content, "\n")

	re := regexp.MustCompile(`(\w+) (\w+) \(#(\w+)\)`)

	row, col := 0, 0
	edges := make(Edges)
	edges.add(Edge{0, 0})

	for _, line := range data {
		matches := re.FindStringSubmatch(line)
		direction := matches[1]
		amount, _ := strconv.Atoi(matches[2])

		for step := 0; step < amount; step++ {
			row += STEPS[direction][0]
			col += STEPS[direction][1]
			edges.add(Edge{row, col})
		}
	}

	min_row := math.MaxInt
	max_row := math.MinInt
	min_col := math.MaxInt
	max_col := math.MinInt

	for edge := range edges {
		min_row = min(min_row, edge.row)
		max_row = max(max_row, edge.row)
		min_col = min(min_col, edge.col)
		max_col = max(max_col, edge.col)
	}

	inside := make(Edges)

	queue := Queue{{1, 1, 0}}
	visited := make(Edges)
	visited.add(Edge{1, 1})

	for !queue.isEmpty() {
		item := queue.Pop()
		row, col, count := item.row, item.col, item.count
		inside.add(Edge{row, col})

		for _, step := range STEPS {
			step_row := step[0]
			step_col := step[1]
			new_row := row + step_row
			new_col := col + step_col

			if min_row <= new_row && new_row <= max_row && min_col <= new_col && new_col <= max_col {

				key := Edge{new_row, new_col}
				if edges.contains(key) || visited.contains(key) {
					continue
				}

				queue.Push(QueueItem{new_row, new_col, count + 1})
				visited.add(key)
			}
		}
	}
	return len(edges) + len(inside)
}

func main() {
	fmt.Println(solution("./example.txt")) // 62
	fmt.Println(solution("./input.txt"))   // 52035
}
