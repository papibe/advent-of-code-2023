package main

import (
	"container/heap"
	"fmt"
	"os"
	"strings"
)

type HeapItem struct {
	heat    int
	row     int
	col     int
	dir_row int
	dir_col int
	s_steps int
}

// An HeatHeap is a min-heap of ints.
type HeatHeap []HeapItem

func (h HeatHeap) Len() int { return len(h) }

func (h HeatHeap) Less(i, j int) bool {
	return h[i].heat < h[j].heat
}

func (h HeatHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }

func (h *HeatHeap) Push(x any) {
	// Push and Pop use pointer receivers because they modify the slice's length,
	// not just its contents.
	*h = append(*h, x.(HeapItem))
}

func (h *HeatHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

type VisitedItem struct {
	row     int
	col     int
	dir_row int
	dir_col int
	s_steps int
}

type VisitedSet map[VisitedItem]bool

func (v VisitedSet) add(item VisitedItem) {
	v[item] = true
}

var STEPS = [][2]int{{0, 1}, {0, -1}, {-1, 0}, {1, 0}}

func solution(filename string) int {
	raw_data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(raw_data), "\n")
	city_map := strings.Split(content, "\n")
	_ = city_map

	hqueue := &HeatHeap{{0, 0, 0, 0, 0, 0}}
	heap.Init(hqueue)

	visited := make(VisitedSet)
	visited.add(VisitedItem{0, 0, 0, 0, 0})

	destination_row := len(city_map) - 1
	destination_col := len(city_map[0]) - 1

	for hqueue.Len() > 0 {
		item := heap.Pop(hqueue).(HeapItem)

		heat := item.heat
		row, col := item.row, item.col
		dir_row, dir_col := item.dir_row, item.dir_col
		s_steps := item.s_steps

		if row == destination_row && col == destination_col {
			return heat
		}

		for _, step := range STEPS {
			step_row := step[0]
			step_col := step[1]
			new_row := row + step_row
			new_col := col + step_col

			if 0 <= new_row && new_row < len(city_map) && 0 <= new_col && new_col < len(city_map[0]) {
				// can't go back on opposite direction
				if step_row == -dir_row && step_col == -dir_col {
					continue
				}

				// if we already took 3 steps don't continue in this direction
				if step_row == dir_row && step_col == dir_col && item.s_steps >= 3 {
					continue
				}

				// Same direction: increase steps, if not reset steps
				var new_steps int
				if step_row == dir_row && step_col == dir_col {
					new_steps = s_steps + 1
				} else {
					new_steps = 1
				}

				_, is_visited := visited[VisitedItem{new_row, new_col, step_row, step_col, new_steps}]
				if is_visited {
					continue
				}

				new_heat := heat + int(rune(city_map[new_row][new_col])-'0')

				heap.Push(hqueue, HeapItem{new_heat, new_row, new_col, step_row, step_col, new_steps})
				visited.add(VisitedItem{new_row, new_col, step_row, step_col, new_steps})
			}
		}
	}

	fmt.Println("Solution not found")
	return -1
}

func main() {
	fmt.Println(solution("./example1.txt")) // 102
	fmt.Println(solution("./input.txt"))    // 1256
}
