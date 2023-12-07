import math
from typing import List, Tuple


def solution(race_stats: List[Tuple[int, int]]) -> int:
    multiplication: int = 1

    for (time, distance) in race_stats:
        # assert (time**2 - 4 * distance) > 0

        sq = math.sqrt(time**2 - 4 * distance)
        x1 = (time - sq) / 2
        x2 = (time + sq) / 2
        if math.modf(x1)[0] == 0:
            x1 += 1
        if math.modf(x2)[0] == 0:
            x2 -= 1
        multiplication *= math.floor(x2) - math.ceil(x1) + 1

    return multiplication


if __name__ == "__main__":
    # print("Part 1 example:", solution([(7, 9), (15, 40), (30, 200)]))  #
    print("Part 1:", solution([(54, 302), (94, 1476), (65, 1029), (92, 1404)]))  #

    # print("Part 2 example:", solution([(71530, 940200)]))  # 71503
    print("Part 2:", solution([(54946592, 302147610291404)]))  # 42550411
