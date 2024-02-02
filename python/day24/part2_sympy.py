from typing import List, Tuple

import sympy

Hailstone = Tuple[int, int, int, int, int, int]


def solution(filename: str) -> int:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    hails: List[Hailstone] = []
    for line in data:
        position, velocity = line.split(" @ ")
        x, y, z = position.split(", ")
        dx, dy, dz = velocity.split(", ")
        hails.append((int(x), int(y), int(z), int(dx), int(dy), int(dz)))

    x = sympy.symbols("x")
    y = sympy.symbols("y")
    z = sympy.symbols("z")

    dx = sympy.symbols("dx")
    dy = sympy.symbols("dy")
    dz = sympy.symbols("dz")

    time = [sympy.symbols(f"t_{i}") for i in range(len(hails))]

    equations = []
    for i, hail in enumerate(hails):
        xa, ya, za, dxa, dya, dza = hail

        equations.append(x + dx * time[i] - dxa * time[i] - xa)
        equations.append(y + dy * time[i] - dya * time[i] - ya)
        equations.append(z + dz * time[i] - dza * time[i] - za)

        # 9 equations, and 9 variables, so should be solvable
        if i >= 3:
            break

    solution = sympy.solve(equations)
    return int(solution[0][x]) + int(solution[0][y]) + int(solution[0][z])


if __name__ == "__main__":
    print(solution("./example.txt"))  # 47
    print(solution("./input.txt"))  # 618534564836937
