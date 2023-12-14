CHANGE = {
     "#": ".",
     ".": "#",
}

def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        patterns: str = fp.read().split("\n\n")


    all_patterns = []
    verticals = []
    horizontals = []
    for index, raw_pattern in enumerate(patterns):
        pattern_str = raw_pattern.splitlines()
        pattern = []
        for line in pattern_str:
            pattern.append([char for char in line])
        all_patterns.append(pattern)
        
        for row in pattern:
            print(row)
        print("=" * 40)

        # check vertical reflection
        for col in range(len(pattern[0]) - 1):
                left = col
                right = col + 1
                # print(f"{col = }")
                while left >= 0 and right < len(pattern[0]):
                    for row in range(len(pattern)):
                        # print(left, right)
                        if pattern[row][left] != pattern[row][right]:
                            break
                    else:
                        left -= 1
                        right += 1
                        continue
                    break                        
                else:
                    # total_sum += col + 1
                    verticals.append((index, col))


        # print(len(pattern), len(pattern[0]))

        # check horizontal reflection
        for row in range(len(pattern) - 1):
                up = row
                down = row + 1
                # print(f"{col = }")
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
                    # total_sum += (row + 1) * 100
                    horizontals.append((index, row))

    total_sum = 0
    print(f"{verticals = }")
    print(f"{horizontals = }")
    #####################################
    for index, old_col in verticals:
        pattern = all_patterns[index]
        found = False
        for i, line in enumerate(pattern):
            for j, cell in enumerate(line):
                # print(f"value: {pattern[i][j]}")
                pattern[i][j] = CHANGE[cell]
                # print(f"change to: {pattern[i][j]}")

                if found:
                    continue
                for row in range(len(pattern) - 1):
                    up = row
                    down = row + 1
                    # print(f"{col = }")
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
                        print(f"{i = } {j = }")
                        print(f"-> {row + 1}, {(row + 1) * 100}")
                        for r in pattern:
                            print(r)
                        print("=" * 40)                        
                        total_sum += (row + 1) * 100
                        found = True

                # check vertical reflection
                for col in range(len(pattern[0]) - 1):
                    left = col
                    right = col + 1
                    # print(f"{col = }")
                    while left >= 0 and right < len(pattern[0]):
                        for row in range(len(pattern)):
                            # print(left, right)
                            if pattern[row][left] != pattern[row][right]:
                                break
                        else:
                            left -= 1
                            right += 1
                            continue
                        break                        
                    else:
                        if col != old_col:
                            print(f"{i = } {j = }")
                            # print(left, right, pattern[i][j])
                            print(f"-> {col + 1}")
                            total_sum += col + 1
                            found = True

                pattern[i][j] = cell
                # print(f" back to: {pattern[i][j]}")


    print("*" * 40)
    ############################
    for index, old_row in horizontals:
        pattern = all_patterns[index]
        found = False

        for i, line in enumerate(pattern):
            for j, cell in enumerate(line):
                pattern[i][j] = CHANGE[cell]

                if found:
                    continue
                for row in range(len(pattern) - 1):
                    up = row
                    down = row + 1
                    # print(f"{col = }")
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
                        if row != old_row:
                            print(f"-> {row + 1}, {(row + 1) * 100}")
                            total_sum += (row + 1) * 100
                            found = True


                # check vertical reflection
                for col in range(len(pattern[0]) - 1):
                    left = col
                    right = col + 1
                    # print(f"{col = }")
                    while left >= 0 and right < len(pattern[0]):
                        for row in range(len(pattern)):
                            # print(left, right)
                            if pattern[row][left] != pattern[row][right]:
                                break
                        else:
                            left -= 1
                            right += 1
                            continue
                        break                        
                    else:
                        print(f"-> {col + 1}")
                        total_sum += col + 1
                        found = True
                        # verticals.append(index)
                pattern[i][j] = cell


    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  #
    print(solution("./input.txt"))  # 
