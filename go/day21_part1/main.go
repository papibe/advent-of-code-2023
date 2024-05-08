package main

import (
	"fmt"
	"os"
	"strings"
)

const WALL = '#'

var STEPS = []Coords{{0, 1}, {0, -1}, {-1, 0}, {1, 0}}

type Coords struct {
	row int
	col int
}

type CoordSet map[Coords]bool

func (set CoordSet) add(coord Coords) {
	set[coord] = true
}

type DequeKey struct {
	coord_set CoordSet
	steps     int
}

type Deque []DequeKey

func (q *Deque) append(dk DequeKey) {
	(*q) = append((*q), dk)
}

func (q Deque) isEmpty() bool {
	return len(q) == 0
}

func (q *Deque) popleft() (CoordSet, int) {
	item := (*q)[0]
	(*q) = (*q)[1:]
	return item.coord_set, item.steps
}

func solution(filename string, max_steps int) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	garden := strings.Split(content, "\n")

	start_row := 0
	start_col := 0
	for row, line := range garden {
		for col, cell := range line {
			if cell == 'S' {
				start_row = row
				start_col = col
				break
			}
		}
	}

	start_coord := Coords{start_row, start_col}
	coords := make(CoordSet)
	coords.add(start_coord)
	queue := make(Deque, 0)
	queue.append(DequeKey{coords, 0})

	final_coords := make(CoordSet)
	for !queue.isEmpty() {
		coords, step_count := queue.popleft()

		if step_count == max_steps {
			final_coords = coords
			break
		}
		next_coords := make(CoordSet)
		for coord, _ := range coords {
			for _, step := range STEPS {
				new_row := coord.row + step.row
				new_col := coord.col + step.col

				if 0 <= new_row && new_row < len(garden) && 0 <= new_col && new_col < len(garden[0]) {
					if garden[new_row][new_col] == WALL {
						continue
					}
					next_coords.add(Coords{new_row, new_col})
				}
			}
		}
		queue.append(DequeKey{next_coords, step_count + 1})
	}
	return len(final_coords)
}

func main() {
	fmt.Println(solution("./example.txt", 6)) // 16
	fmt.Println(solution("./input.txt", 64))  // 3682
}
