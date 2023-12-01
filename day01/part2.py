DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    addition: int = 0
    for line in data:
        numbers = {}

        # check for spelled out digits
        for k, v in DIGITS.items():
            index = line.find(k)

            # check for ALL occurrences of a digit
            while index >= 0:
                numbers[index] = v
                index = line.find(k, index + len(k))

        # check for ascii digits
        for index, char in enumerate(line):
            if char.isnumeric():
                numbers[index] = int(char)

        # get first and last indexes
        min_index = len(line)
        max_index = -1
        for index in numbers.keys():
            max_index = max(max_index, index)
            min_index = min(min_index, index)

        # addition += (numbers[min(numbers.keys())] * 10) + numbers[max(numbers.keys())]
        addition += (numbers[min_index] * 10) + numbers[max_index]

    return addition


if __name__ == "__main__":
    # print(solution("./example2.txt")) # 281
    print(solution("./input.txt"))  # 54203
