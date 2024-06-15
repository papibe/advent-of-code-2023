package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

const WALL = '#'

const NONE = -1

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
	coord Coords
	steps int
}

type Deque []DequeKey

func (q *Deque) append(dk DequeKey) {
	(*q) = append((*q), dk)
}

func (q Deque) isEmpty() bool {
	return len(q) == 0
}

func (q *Deque) popleft() (Coords, int) {
	item := (*q)[0]
	(*q) = (*q)[1:]
	return item.coord, item.steps
}

func garden_count(start_row, start_col int, garden []string) [][]int {

	size := len(garden)

	start_coord := Coords{start_row, start_col}

	visited := make(CoordSet)
	visited.add(start_coord)

	queue := make(Deque, 0)
	queue.append(DequeKey{start_coord, 0})

	distances := [][]int{}
	for i := 0; i < size; i++ {
		row := []int{}
		for j := 0; j < size; j++ {
			row = append(row, NONE)
		}
		distances = append(distances, row)
	}

	for !queue.isEmpty() {
		coords, current_distance := queue.popleft()
		row, col := coords.row, coords.col

		distances[row][col] = current_distance

		for _, step := range STEPS {
			new_row := row + step.row
			new_col := col + step.col
			new_distance := current_distance + 1

			if 0 <= new_row && new_row < size && 0 <= new_col && new_col < size {
				new_coords := Coords{new_row, new_col}
				_, is_visited := visited[new_coords]
				if garden[new_row][new_col] == '.' && !is_visited {
					queue = append(queue, DequeKey{new_coords, new_distance})
					visited.add(new_coords)
				}
			}
		}
	}

	return distances
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

	size := len(garden)
	distances := garden_count(start_row, start_col, garden)

	shortest_distance_to_edges := math.MaxInt
	for row := 0; row < size; row++ {
		shortest_distance_to_edges = min(shortest_distance_to_edges, distances[row][0])
	}

	diameter := int((max_steps - shortest_distance_to_edges) / size)

	odd_grid := 0
	even_grid := 0
	odd_corner := 0
	even_corner := 0

	for _, row := range distances {
		for _, distance := range row {
			if distance == NONE {
				continue
			}
			if distance%2 == 0 {
				even_grid += 1
				if distance > shortest_distance_to_edges {
					even_corner += 1
				}
			} else {
				odd_grid += 1
				if distance > shortest_distance_to_edges {
					odd_corner += 1
				}
			}
		}
	}

	return int(math.Pow(float64(diameter+1), 2)*float64(odd_grid) + math.Pow(float64(diameter), 2)*float64(even_grid) - (float64(diameter)+1)*float64(odd_corner) + float64(diameter)*float64(even_corner))
}

func main() {
	fmt.Println(solution("./input.txt", 26501365)) // 609012263058042
}
