from typing import List, Tuple

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


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    total_sum: int = 0

    for row in range(len(data)):
        line: str = data[row]

        # check all the line for part numbers
        index: int = 0
        while index < len(line):
            start: int = index
            while index < len(line) and line[index].isnumeric():
                index += 1

            if line[start].isnumeric() and line[index - 1].isnumeric():

                near_symbol: bool = False
                for col in range(start, index):
                    for row_step, col_step in STEPS:
                        new_row: int = row + row_step
                        new_col: int = col + col_step

                        if 0 <= new_row < len(data) and 0 <= new_col < len(line):
                            if (not data[new_row][new_col].isnumeric()) and data[
                                new_row
                            ][new_col] != ".":
                                near_symbol = True

                if near_symbol:
                    total_sum += int(line[start:index])

            index += 1

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 4361
    print(solution("./input.txt"))  # 519444
