def solution(filename: str, expanding_factor: int) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    galaxies = []
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if char == "#":
                galaxies.append([row, col])

    expanding_rows = []
    for row, line in enumerate(data):
        for char in line:
            if char != ".":
                break
        else:
            expanding_rows.append(row)

    expanding_cols = []
    for col in range(len(data[0])):
        for row in range(len(data)):
            if data[row][col] != ".":
                break
        else:
            expanding_cols.append(col)

    # expand rows
    while expanding_rows:
        expanding_row = expanding_rows.pop()
        for index, (row, col) in enumerate(galaxies):
            if row > expanding_row:
                galaxies[index][0] += expanding_factor - 1
        for i in range(len(expanding_rows)):
            if expanding_rows[i] > expanding_row:
                expanding_rows[i] += expanding_factor - 1

    # expand cols
    while expanding_cols:
        expanding_col = expanding_cols.pop()
        for index, (row, col) in enumerate(galaxies):
            if col > expanding_col:
                galaxies[index][1] += expanding_factor - 1
        for i in range(len(expanding_cols)):
            if expanding_cols[i] > expanding_col:
                expanding_cols[i] += expanding_factor - 1

    total_sum = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            total_sum += abs(galaxies[i][0] - galaxies[j][0]) + abs(
                galaxies[i][1] - galaxies[j][1]
            )

    return total_sum


if __name__ == "__main__":
    # print("Part 1 example:", solution("./example.txt", 2))  # 374
    # print("Part 2 example1:", solution("./example.txt", 10))  # 1030
    # print("Part 2 example2:", solution("./example.txt", 100))  # 8410

    print("Part 1:", solution("./input.txt", 2))  # 9734203
    print("Part 2:", solution("./input.txt", 1000000))  # 568914596391
