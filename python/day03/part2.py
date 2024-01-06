from typing import List, Set, Tuple

STEPS: List[Tuple[int, int]] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def get_unique_number_id(data: List[str], row: int, col: int) -> Tuple[int, int, int]:
    start: int = col
    while start >= 0 and data[row][start].isnumeric():
        start -= 1
    if start < 0:
        start = 0
    else:
        start += 1
    end: int = col
    while end < len(data[row]) and data[row][end].isnumeric():
        end += 1

    return (row, start, end)


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    total_sum: int = 0

    for row in range(len(data)):
        line: str = data[row]

        for index, char in enumerate(line):
            if line[index] == "*":

                # collect all unique adjacent parts
                parts: Set[Tuple[int, int, int]] = set()
                for row_step, col_step in STEPS:
                    new_row: int = row + row_step
                    new_col: int = index + col_step

                    if 0 <= new_row < len(data) and 0 <= new_col < len(line):
                        if data[new_row][new_col].isnumeric():
                            part_id = get_unique_number_id(data, new_row, new_col)
                            parts.add(part_id)

                if len(parts) == 2:
                    ratio: int = 1
                    for (number_row, start, end) in parts:
                        ratio *= int(data[number_row][start:end])

                    total_sum += ratio

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 467835
    print(solution("./input.txt"))  # 74528807
