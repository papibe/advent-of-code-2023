def solution(filename: str, lower, high) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    hailstones = []
    for line in data:
        position, velocity = line.split(" @ ")
        x, y, z = position.split(", ")
        dx, dy, dz = velocity.split(", ")
        hailstones.append((int(x), int(y), int(z), int(dx), int(dy), int(dz)))

    number_of_hailstones = len(hailstones)
    intersections = 0
    for i in range(number_of_hailstones):
        for j in range(i + 1, number_of_hailstones):

            # use y = m*x + c  form to represent a line in xy plane:
            # first line (i) ya = dxa*x + xa
            # second line (j) yb = dxb*x + xb
            xa, ya, _, dxa, dya, _ = hailstones[i]
            xb, yb, _, dxb, dyb, _ = hailstones[j]

            ma = dya / dxa
            mb = dyb / dxb
            ca = ya - ma * xa
            cb = yb - mb * xb

            if ma != mb:
                xi = (cb - ca) / (ma - mb)
                yi = (xi * ma) + ca

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
