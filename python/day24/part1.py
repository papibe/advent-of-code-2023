from typing import List, Tuple

Hailstone = Tuple[int, int, int, int, int, int]


def solution(filename: str, lower: int, high: int) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    hailstones: List[Hailstone] = []
    for line in data:
        position, velocity = line.split(" @ ")
        x, y, z = position.split(", ")
        dx, dy, dz = velocity.split(", ")
        hailstones.append((int(x), int(y), int(z), int(dx), int(dy), int(dz)))

    number_of_hailstones = len(hailstones)
    intersections: int = 0
    for i in range(number_of_hailstones):
        for j in range(i + 1, number_of_hailstones):

            # use y = m*x + c  form to represent a line in xy plane:
            # first line (i) ya = dxa*x + xa
            # second line (j) yb = dxb*x + xb
            xa, ya, _, dxa, dya, _ = hailstones[i]
            xb, yb, _, dxb, dyb, _ = hailstones[j]

            ma: float = dya / dxa
            mb: float = dyb / dxb
            ca: float = ya - ma * xa
            cb: float = yb - mb * xb

            if ma != mb:
                xi: float = (cb - ca) / (ma - mb)
                yi: float = (xi * ma) + ca

                if (
                    lower <= xi <= high
                    and lower <= yi <= high
                    and (xi > xa) == (xa + dxa > xa)
                    and (xi > xb) == (xb + dxb > xb)
                ):
                    intersections += 1

    return intersections


if __name__ == "__main__":
    print(solution("./example.txt", 7, 27))  # 2
    print(solution("./input.txt", 200000000000000, 400000000000000))  # 13910
