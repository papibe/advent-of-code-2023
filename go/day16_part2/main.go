package main

import (
	"fmt"
	"os"
	"strings"
)

type Direction struct {
	row int
	col int
}

type Position Direction

var RIGHT = Direction{0, 1}
var LEFT = Direction{0, -1}
var UP = Direction{-1, 0}
var DOWN = Direction{1, 0}

var RULES = map[Direction]map[rune][]Direction{
	RIGHT: {
		'.':  []Direction{RIGHT},
		'/':  []Direction{UP},
		'\\': []Direction{DOWN},
		'|':  []Direction{UP, DOWN},
		'-':  []Direction{RIGHT},
	},
	LEFT: {
		'.':  []Direction{LEFT},
		'/':  []Direction{DOWN},
		'\\': []Direction{UP},
		'|':  []Direction{UP, DOWN},
		'-':  []Direction{LEFT},
	},
	UP: {
		'.':  []Direction{UP},
		'/':  []Direction{RIGHT},
		'\\': []Direction{LEFT},
		'|':  []Direction{UP},
		'-':  []Direction{LEFT, RIGHT},
	},
	DOWN: {
		'.':  []Direction{DOWN},
		'/':  []Direction{LEFT},
		'\\': []Direction{RIGHT},
		'|':  []Direction{DOWN},
		'-':  []Direction{LEFT, RIGHT},
	},
}

type VisitedKey struct {
	position  Position
	direction Direction
}

type VisitedSet map[VisitedKey]bool

func (v VisitedSet) add(k VisitedKey) {
	v[k] = true
}

type Deque []VisitedKey

func (q *Deque) popleft() (Position, Direction) {
	item := (*q)[0]
	(*q) = (*q)[1:]
	return item.position, item.direction
}

func solution(filename string) int {
	data, err := os.ReadFile(filename)

	if err != nil {
		panic("file error")
	}
	content := strings.Trim(string(data), "\n")
	contraption := strings.Split(content, "\n")

	max_energy := 0
	for col := 0; col < len(contraption[0]); col++ {
		max_energy = max(max_energy, solve(contraption, Position{0, col}, DOWN))
		max_energy = max(
			max_energy, solve(contraption, Position{len(contraption) - 1, col}, UP))
	}
	for row := 0; row < len(contraption); row++ {
		max_energy = max(max_energy, solve(contraption, Position{row, 0}, LEFT))
		max_energy = max(
			max_energy, solve(contraption, Position{row, len(contraption[0]) - 1}, RIGHT))
	}
	return max_energy
}

func solve(contraption []string, position Position, direction Direction) int {
	// BFS init
	queue := Deque{{position, direction}}
	visited := make(VisitedSet)
	energized := make(map[Position]bool)

	for len(queue) > 0 {
		pos, direction := queue.popleft()
		energized[pos] = true

		cell := contraption[pos.row][pos.col]
		next_directions := RULES[direction][rune(cell)]

		for _, dir := range next_directions {
			new_pos := Position{pos.row + dir.row, pos.col + dir.col}
			_, is_visited := visited[VisitedKey{new_pos, dir}]
			if 0 <= new_pos.row &&
				new_pos.row < len(contraption) &&
				0 <= new_pos.col &&
				new_pos.col < len(contraption[0]) &&
				!is_visited {

				queue = append(queue, VisitedKey{new_pos, dir})
				visited.add(VisitedKey{new_pos, dir})
			}
		}
	}

	return len(energized)
}

func main() {
	fmt.Println(solution("./example.txt")) // 51
	fmt.Println(solution("./input.txt"))   // 7987
}
