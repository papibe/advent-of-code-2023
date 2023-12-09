from collections import deque


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    sequences = []
    for line in data:
        int_seq = [int(n) for n in line.split(" ")]
        sequences.append(deque(int_seq))

    total_sum = 0

    for sequence in sequences:
        triangle = [sequence]

        prev_row = triangle[-1]
        while any(n != 0 for n in prev_row):
            next_row = deque([0] * (len(prev_row) - 1))
            for i in range(len(prev_row) - 1):
                next_row[i] = prev_row[i + 1] - prev_row[i]
            triangle.append(next_row)
            prev_row = triangle[-1]

        triangle[-1].appendleft(0)
        for i in range(len(triangle) - 2, -1, -1):
            triangle[i].appendleft(triangle[i][0] - triangle[i + 1][0])

        total_sum += triangle[0][0]

    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 2
    print(solution("./input.txt"))  # 1089
