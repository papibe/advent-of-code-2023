#
# Working solution. Will refactor soon
#

import re
from collections import deque


landscape = {
    "|": [(1, 0), (-1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(1, 0), (0, 1)],
    ".": [],
    "S": [],
}

START = "S"
SPACE = "."

STEPS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

GOOD_CORNER = {
    (-1, 0): "-",  # up
    (1, 0): "-",  # down
    (0, -1): "|",  # left
    (0, 1): "|",  # right
    (-1, -1): "F",  # nw
    (-1, 1): "7",  # ne
    (1, -1): "L",  # nw
    (1, 1): "J",  # ne
}


def solution(filename: str, s_form: str) -> int:
    with open(filename, "r") as fp:
        raw_data: str = fp.read().splitlines()

    mdata = []
    for line in raw_data:
        mdata.append([char for char in line])

    # patch S
    # find start
    for row, line in enumerate(mdata):
        for col, char in enumerate(line):
            if char == START:
                start_row = 2* row
                start_col = 2* col
                mdata[row][col] = s_form
        else:
            continue
        break

    # print(len(mdata), len(mdata[0]))

    data = []
    for _ in range(2*len(mdata)):
        data.append([{"value": ".", "original": False} for _ in range(2 * len(mdata[0]))])
    # data = [[{"value": ".", "original": False}] * (2 * len(mdata[0])) for _ in range(2*len(mdata))]

    for row, line in enumerate(mdata):
        for col, char in enumerate(line):
            data[2 * row][2 * col] = {"value": char, "original": True}

    # for row in data:
    #     for item in row:
    #         print(item["value"], end="")
    #     print()
    # print("================================")


    for row, line in enumerate(data):
        for col, item in enumerate(line):
            if not item["original"]:
                # data[row][col]["value"] = "*"
                # print(row, col)
                # is connected

                if 0 <= col - 1 and col + 1 < len(data[0]):
                    if (
                        (data[row][col - 1]["value"] == "-" and data[row][col + 1]["value"] == "-")
                        or (data[row][col - 1]["value"] == "-" and data[row][col + 1]["value"] == "7")
                        or (data[row][col - 1]["value"] == "-" and data[row][col + 1]["value"] == "J")
                        or (data[row][col - 1]["value"] == "F" and data[row][col + 1]["value"] == "-")
                        or (data[row][col - 1]["value"] == "F" and data[row][col + 1]["value"] == "7")
                        or (data[row][col - 1]["value"] == "F" and data[row][col + 1]["value"] == "J")
                        or (data[row][col - 1]["value"] == "L" and data[row][col + 1]["value"] == "-")
                        or (data[row][col - 1]["value"] == "L" and data[row][col + 1]["value"] == "7")
                        or (data[row][col - 1]["value"] == "L" and data[row][col + 1]["value"] == "J")
                        ):
                        # print("\tchanged")
                        data[row][col]["value"] = "-"
                        # print(row, col)

                if 0 <= row - 1 and row + 1 < len(data):
                    if (
                        (data[row - 1][col]["value"] == "F" and data[row + 1][col]["value"] == "|")
                        or (data[row - 1][col]["value"] == "F" and data[row + 1][col]["value"] == "L")
                        or (data[row - 1][col]["value"] == "F" and data[row + 1][col]["value"] == "J")
                        or (data[row - 1][col]["value"] == "|" and data[row + 1][col]["value"] == "|")
                        or (data[row - 1][col]["value"] == "|" and data[row + 1][col]["value"] == "L")
                        or (data[row - 1][col]["value"] == "|" and data[row + 1][col]["value"] == "J")
                        or (data[row - 1][col]["value"] == "7" and data[row + 1][col]["value"] == "|")
                        or (data[row - 1][col]["value"] == "7" and data[row + 1][col]["value"] == "J")
                        or (data[row - 1][col]["value"] == "7" and data[row + 1][col]["value"] == "L")

                        ):
                        # print("\tchanged")
                        data[row][col]["value"] = "|"
                        # print(row, col)


        # else:
        #     continue
        # break

    

    for row in data:
        for item in row:
            print(item["value"], end="")
        print()
    print("================================")


    #######################################################
    # marking inside the loop
    queue = deque([(start_row, start_col, 0)])
    visited = set([(start_row, start_col)])

    print(start_row, start_col)

    while queue:
        row, col, steps = queue.popleft()
        data[row][col]["pipe"] = True

        for (nrow, ncol) in landscape[data[row][col]["value"]]:
            new_row = row + nrow
            new_col = col + ncol
            if 0 <= new_row <= len(data) and 0 <= new_col < len(data[0]):

                if data[row][col]["value"] != "." and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))

    #######################################################


    for row, line in enumerate(data):
        for col, item in enumerate(line):
            if "pipe" not in item:
                data[row][col]["value"] = "."


    for row in data:
        for item in row:
            print(item["value"], end="")
        print()
    print("================================")


    visited = set()
    counter = 0

    outside = set()

    print(visited)

    for row, line in enumerate(data):
        for col, char in enumerate(line):
            if (row, col) not in visited and data[row][col]["value"] == SPACE:
                bfs_row = row
                bfs_col = col
                print(f"{bfs_row = }, {bfs_col}")
                queue = deque([(bfs_row, bfs_col)])
                local_visited = set([(bfs_row, bfs_col)])
                contained = True
                while queue:
                    bfs_row, bfs_col = queue.popleft()
                    for row_step, col_step in STEPS:
                        new_row = bfs_row + row_step
                        new_col = bfs_col + col_step
                        if (new_row, new_col) in outside:
                            contained = False
                        if 0 <= new_row < len(data) and 0 <= new_col < len(data[0]):
                            if (
                                data[new_row][new_col]["value"] == SPACE
                                and (new_row, new_col) not in local_visited
                            ):
                                queue.append((new_row, new_col))
                                local_visited.add((new_row, new_col))
                        else:
                            contained = False
                if contained:
                    # counter += len(local_visited)
                    print(local_visited, len(local_visited))
                    for r, c in local_visited:
                        if data[r][c]["original"]:
                            counter += 1
                else:
                    outside.update(local_visited)
                visited.update(local_visited)

    return counter


if __name__ == "__main__":
    # print(solution("./example0.txt", "F"))  #
    # print(solution("./example3.txt", "F"))  #
    # print(solution("./example4.txt", "F")) #
    # print(solution("./example5.txt", "F")) #
    # print(solution("./example6.txt", "7")) #
    print(solution("./input.txt", "|"))  #
