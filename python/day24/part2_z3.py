import z3

def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: str = fp.read().splitlines()

    hails = []
    for line in data:
        position, velocity = line.split(" @ ")
        x, y, z = position.split(", ")
        dx, dy, dz = velocity.split(", ")
        hails.append((int(x), int(y), int(z), int(dx), int(dy), int(dz)))

    x = z3.Int("x")
    y = z3.Int("y")
    z = z3.Int("z")

    dx = z3.Int("dx")
    dy = z3.Int("dy")
    dz = z3.Int("dz")

    time = [z3.Int(f"t_{i}") for i in range(len(hails))]

    solver = z3.Solver()
    for i, hail in enumerate(hails):
        xa, ya, za, dxa, dya, dza = hail

        solver.add(x + dx * time[i] == dxa * time[i] + xa)
        solver.add(y + dy * time[i] == dya * time[i] + ya)
        solver.add(z + dz * time[i] == dza * time[i] + za)

    solution = solver.check()
    model = solver.model()

    return model.eval(x + y + z)


if __name__ == "__main__":
    print(solution("./example.txt"))  # 47
    print(solution("./input.txt"))  # 618534564836937
