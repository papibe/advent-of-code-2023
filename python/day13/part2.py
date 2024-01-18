from typing import List, Tuple

CHANGE = {
    "#": ".",
    ".": "#",
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        patterns: List[str] = fp.read().split("\n\n")

    all_patterns: List[List[List[str]]] = []
    verticals: List[Tuple[int, int]] = []
    horizontals: List[Tuple[int, int]] = []

    for index, raw_pattern in enumerate(patterns):
        pattern_str: List[str] = raw_pattern.splitlines()
        pattern: List[List[str]] = []
        for line in pattern_str:
            pattern.append([char for char in line])
        all_patterns.append(pattern)

        # check vertical reflection
        for col in range(len(pattern[0]) - 1):
            left: int = col
            right: int = col + 1
            while left >= 0 and right < len(pattern[0]):
                for row in range(len(pattern)):
                    if pattern[row][left] != pattern[row][right]:
                        break
                else:
                    left -= 1
                    right += 1
                    continue
                break
            else:
                verticals.append((index, col))

        # check horizontal reflection
        for row in range(len(pattern) - 1):
            up: int = row
            down: int = row + 1
            while up >= 0 and down < len(pattern):
                for col in range(len(pattern[0])):
                    if pattern[up][col] != pattern[down][col]:
                        break
                else:
                    up -= 1
                    down += 1
                    continue
                break
            else:
                horizontals.append((index, row))

    total_sum: int = 0
    for index, old_col in verticals:
        pattern = all_patterns[index]
        found: bool = False
        for i, line_ in enumerate(pattern):
            for j, cell in enumerate(line_):
                pattern[i][j] = CHANGE[cell]

                if found:
                    continue
                for row in range(len(pattern) - 1):
                    up = row
                    down = row + 1
                    while up >= 0 and down < len(pattern):
                        for col in range(len(pattern[0])):
                            # print(f"{up = }, {down = }, {col = }")
                            if pattern[up][col] != pattern[down][col]:
                                break
                        else:
                            up -= 1
                            down += 1
                            continue
                        break
                    else:
                        total_sum += (row + 1) * 100
                        found = True

                # check vertical reflection
                for col in range(len(pattern[0]) - 1):
                    left = col
                    right = col + 1
                    while left >= 0 and right < len(pattern[0]):
                        for row in range(len(pattern)):
                            if pattern[row][left] != pattern[row][right]:
                                break
                        else:
                            left -= 1
                            right += 1
                            continue
                        break
                    else:
                        if col != old_col:
                            total_sum += col + 1
                            found = True

                pattern[i][j] = cell

    for index, old_row in horizontals:
        pattern = all_patterns[index]
        found = False

        for i, line_2 in enumerate(pattern):
            for j, cell in enumerate(line_2):
                pattern[i][j] = CHANGE[cell]

                if found:
                    continue
                for row in range(len(pattern) - 1):
                    up = row
                    down = row + 1
                    while up >= 0 and down < len(pattern):
                        for col in range(len(pattern[0])):
                            if pattern[up][col] != pattern[down][col]:
                                break
                        else:
                            up -= 1
                            down += 1
                            continue
                        break
                    else:
                        if row != old_row:
                            total_sum += (row + 1) * 100
                            found = True

                # check vertical reflection
                for col in range(len(pattern[0]) - 1):
                    left = col
                    right = col + 1
                    while left >= 0 and right < len(pattern[0]):
                        for row in range(len(pattern)):
                            if pattern[row][left] != pattern[row][right]:
                                break
                        else:
                            left -= 1
                            right += 1
                            continue
                        break
                    else:
                        total_sum += col + 1
                        found = True
                pattern[i][j] = cell

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 400
    print(solution("./input.txt"))  # 32312
