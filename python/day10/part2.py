from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Set, Tuple

Direction = Tuple[int, int]

LEFT: Direction = (0, -1)
RIGHT: Direction = (0, 1)
UP: Direction = (-1, 0)
DOWN: Direction = (1, 0)

landscape: Dict[str, List[Direction]] = {
    "|": [UP, DOWN],
    "-": [LEFT, RIGHT],
    "L": [UP, RIGHT],
    "J": [UP, LEFT],
    "7": [LEFT, DOWN],
    "F": [RIGHT, DOWN],
    ".": [],
}

START: str = "S"
SPACE: str = "."

STEPS: List[Direction] = [
    LEFT,
    RIGHT,
    UP,
    DOWN,
]


@dataclass
class Cell:
    value: str
    is_original: bool = False
    in_pipe: bool = False


def parse(filename: str) -> List[List[str]]:
    with open(filename, "r") as fp:
        raw_data: List[str] = fp.read().splitlines()

    grid: List[List[str]] = []
    for line in raw_data:
        grid.append([char for char in line])

    return grid


def get_start_coords(grid: List[List[str]]) -> Tuple[int, int]:
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == START:
                return (row, col)
    return (-1, -1)


def build_double_grid(original_grid: List[List[str]]) -> List[List[Cell]]:
    grid: List[List[Cell]] = []
    for _ in range(2 * len(original_grid)):
        grid.append([Cell(value=SPACE) for _ in range(2 * len(original_grid[0]))])

    for row, line_ in enumerate(original_grid):
        for col, char in enumerate(line_):
            grid[2 * row][2 * col].value = char
            grid[2 * row][2 * col].is_original = True

    for row, line in enumerate(grid):
        for col, item in enumerate(line):
            if item.is_original or item.value != SPACE:
                continue

            if 0 <= col - 1 and col + 1 < len(grid[0]):
                left_neighbor = grid[row][col - 1].value
                right_neighbor = grid[row][col + 1].value
                if (
                    RIGHT in landscape[left_neighbor]
                    and LEFT in landscape[right_neighbor]
                ):
                    grid[row][col].value = "-"

            if 0 <= row - 1 and row + 1 < len(grid):
                up_neighbor = grid[row - 1][col].value
                down_neighbor = grid[row + 1][col].value
                if DOWN in landscape[up_neighbor] and UP in landscape[down_neighbor]:
                    grid[row][col].value = "|"

    return grid


def solve(start_row: int, start_col: int, grid: List[List[Cell]]) -> int:
    # marking elements that are part of the loop
    queue: Deque[Tuple[int, int, int]] = deque([(start_row, start_col, 0)])
    visited: Set[Tuple[int, int]] = set([(start_row, start_col)])

    while queue:
        row, col, steps = queue.popleft()
        grid[row][col].in_pipe = True

        for (nrow, ncol) in landscape[grid[row][col].value]:
            new_row: int = row + nrow
            new_col: int = col + ncol
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):

                if grid[row][col].value != SPACE and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))

    for row, line in enumerate(grid):
        for col, item in enumerate(line):
            if not item.in_pipe:
                grid[row][col].value = SPACE

    # count contained cells
    counter: int = 0
    visited = set()
    outside: Set[Tuple[int, int]] = set()

    for row, line in enumerate(grid):
        for col, cell in enumerate(line):
            if (row, col) not in visited and cell.value == SPACE:
                bfs_row: int = row
                bfs_col: int = col

                queue_: Deque[Tuple[int, int]] = deque([(bfs_row, bfs_col)])
                local_visited: Set[Tuple[int, int]] = set([(bfs_row, bfs_col)])
                contained: bool = True

                while queue_:
                    bfs_row, bfs_col = queue_.popleft()
                    for row_step, col_step in STEPS:
                        new_row = bfs_row + row_step
                        new_col = bfs_col + col_step
                        if (new_row, new_col) in outside:
                            contained = False
                        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                            if (
                                grid[new_row][new_col].value == SPACE
                                and (new_row, new_col) not in local_visited
                            ):
                                queue_.append((new_row, new_col))
                                local_visited.add((new_row, new_col))
                        else:
                            contained = False

                if contained:
                    for r, c in local_visited:
                        if grid[r][c].is_original:
                            counter += 1
                else:
                    outside.update(local_visited)
                visited.update(local_visited)

    return counter


def solution(filename: str, start_form: str) -> int:
    # parse file
    original_grid: List[List[str]] = parse(filename)

    # get start position
    start_row, start_col = get_start_coords(original_grid)

    # patch start position with its proper shape
    original_grid[start_row][start_col] = start_form

    # new position for double grid:
    start_row *= 2
    start_col *= 2

    # build double sized grid
    grid: List[List[Cell]] = build_double_grid(original_grid)

    return solve(start_row, start_col, grid)


if __name__ == "__main__":
    print(solution("./example0.txt", "F"))  # 0
    print(solution("./example1.txt", "F"))  # 1
    print(solution("./example2.txt", "F"))  # 1
    print(solution("./example3.txt", "F"))  # 4
    print(solution("./example4.txt", "F"))  # 4
    print(solution("./example5.txt", "F"))  # 8
    print(solution("./example6.txt", "7"))  # 10
    print(solution("./input.txt", "|"))  # 303
