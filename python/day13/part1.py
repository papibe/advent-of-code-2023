def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        patterns: str = fp.read().split("\n\n")

    total_sum = 0
    for raw_pattern in patterns:
        pattern_str = raw_pattern.splitlines()

        pattern = []
        for line in pattern_str:
            pattern.append([char for char in line])
        
        # for row in pattern:
        #     print(row)
        # print("=" * 40)

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
                # print(f" -> {col + 1}")
                total_sum += col + 1


        # print(len(pattern), len(pattern[0]))

        # check vertical reflection
        for row in range(len(pattern) - 1):
            up = row
            down = row + 1
            # print(f"{col = }")
            while up >= 0 and down < len(pattern):
                for col in range(len(pattern[0])):
                    # print(left, right)
                    # print(f"{up = }, {down = }, {col = }")
                    if pattern[up][col] != pattern[down][col]:
                        break
                else:
                    up -= 1
                    down += 1
                    continue
                break                        
            else:
                # print(f" -> {row + 1}")
                total_sum += (row + 1) * 100


        pass

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  #
    print(solution("./input.txt"))  # 
