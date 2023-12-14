def get_vertical_reflection(pattern):
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
            return col + 1

    return None


def get_horizontal_reflection(pattern):
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
            return row + 1

    return None


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        patterns: str = fp.read().split("\n\n")

    total_sum = 0
    for raw_pattern in patterns:
        pattern = raw_pattern.splitlines()

        # check vertical reflection
        col = get_vertical_reflection(pattern)
        if col is not None:
            total_sum += col

        # check horizontal reflection
        row = get_horizontal_reflection(pattern)
        if row is not None:
            total_sum += row * 100

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 405
    print(solution("./input.txt"))  # 33122
