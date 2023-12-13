def check(spring, numbers):
    memo = {}

    def _check(current_size, index, nindex):

        key = (current_size, index, nindex)
        if key in memo:
            return memo[key]

        if index == len(spring):
            if nindex == len(numbers):
                return 1
            else:
                return 0

        result = 0
        if spring[index] == "#":
            result += _check(current_size + 1, index + 1, nindex)

        elif (
            spring[index] == "."
            and current_size > 0
            and nindex < len(numbers)
            and current_size == numbers[nindex]
        ):
            result += _check(0, index + 1, nindex + 1)

        elif spring[index] == "." and current_size == 0:
            result += _check(0, index + 1, nindex)

        elif spring[index] == "?":
            # "#"
            result += _check(current_size + 1, index + 1, nindex)
            # "."
            if (
                current_size > 0
                and nindex < len(numbers)
                and current_size == numbers[nindex]
            ):
                result += _check(0, index + 1, nindex + 1)

            elif current_size == 0:
                result += _check(0, index + 1, nindex)

        memo[key] = result
        return result

    return _check(0, 0, 0)


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    total_sum = 0
    for line in data:
        springs, numbers_str = line.split(" ")
        numbers = [int(n) for n in numbers_str.split(",")]

        new_numbers = []
        for _ in range(5):
            new_numbers.extend(numbers)

        new_springs = []
        for _ in range(5):
            new_springs.append(springs)

        # add "." just to easy edge condition
        new_springs_str = "?".join(new_springs) + "."

        total_sum += check(new_springs_str, new_numbers)

    return total_sum


if __name__ == "__main__":
    # print(solution("./example.txt"))  # 525152
    print(solution("./input.txt"))  # 65607131946466
