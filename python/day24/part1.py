def solution(filename: str, lower, high) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    hails = []
    for line in data:
        position, velocity = line.split(" @ ")
        x, y, z = position.split(", ")
        vx, vy, vz = velocity.split(", ")
        hails.append((int(x), int(y), int(z), int(vx), int(vy), int(vz)))

    counter = 0
    for i in range(len(hails)):
        for j in range(i + 1, len(hails)):

            xa, ya, za, dxa, dya, dza = hails[i]
            xb, yb, zb, dxb, dyb, dzb = hails[j]

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
                    counter += 1
    return counter


if __name__ == "__main__":
    print(solution("./example.txt", 7, 27))  #
    print(solution("./input.txt", 200000000000000, 400000000000000))  # 13910
