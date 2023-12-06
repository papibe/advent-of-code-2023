from typing import List, Tuple


def solution(race_stats: List[Tuple[int, int]]) -> int:
    multiplication: int = 1

    for (time, distance) in race_stats:
        counter: int = 0
        for hold in range(time + 1):
            speed: int = hold
            my_distance: int = (time - hold) * speed
            if my_distance > distance:
                counter += 1
        multiplication *= counter

    return multiplication


if __name__ == "__main__":
    # print("Part 1 example:", solution([(7, 9), (15, 40), (30, 200)]))  #
    print("Part 1:", solution([(54, 302), (94, 1476), (65, 1029), (92, 1404)]))  #

    # print("Part 2 example:", solution([(71530, 940200)]))  # 71503
    print("Part 2:", solution([(54946592, 302147610291404)]))  # 42550411
