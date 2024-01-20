def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()[0]

    total_sum: int = 0
    for sequence in data.split(","):
        ascii_value: int = 0
        for char in sequence:
            ascii_value += ord(char)
            ascii_value *= 17
            ascii_value %= 256
        total_sum += ascii_value
    return total_sum


if __name__ == "__main__":
    print(solution("./example.txt"))  # 1320
    print(solution("./input.txt"))  # 516070
