import re
from typing import List, Match, Optional


class Cube:
    def __init__(self, x0: int, y0: int, z0: int, x1: int, y1: int, z1: int) -> None:
        self.coords = [x0, y0, z0, x1, y1, z1]
        self.x0: int = x0
        self.y0: int = y0
        self.z0: int = z0
        self.x1: int = x1
        self.y1: int = y1
        self.z1: int = z1

        self.supports_list: List[int] = []
        self.supported_by_list: List[int] = []

    def does_intersects(self, cube: "Cube") -> bool:
        if self.x0 > cube.x1 or self.x1 < cube.x0:
            return False
        if self.y0 > cube.y1 or self.y1 < cube.y0:
            return False
        return True

    def down_to(self, current_floor: int) -> None:
        assert self.z1 >= self.z0

        self.z1 = self.z1 - (self.z0 - current_floor)
        self.z0 = current_floor

    def supports(self, other_cube_index: int) -> None:
        self.supports_list.append(other_cube_index)

    def supported_by(self, other_cube_index: int) -> None:
        self.supported_by_list.append(other_cube_index)

    def __lt__(self, another: "Cube") -> bool:
        return self.z0 < another.z0

    def __repr__(self) -> str:
        return f"({self.x0},{self.y0},{self.z0}) - ({self.x1},{self.y1},{self.z1})"


def parse(filename: str) -> List[Cube]:
    with open(filename, "r") as fp:
        data: List[str] = fp.read().splitlines()

    regex: str = r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)"
    cubes: List[Cube] = []
    for line in data:
        matches: Optional[Match[str]] = re.search(regex, line)

        assert matches is not None
        x0: int = int(matches.group(1))
        y0: int = int(matches.group(2))
        z0: int = int(matches.group(3))

        x1: int = int(matches.group(4))
        y1: int = int(matches.group(5))
        z1: int = int(matches.group(6))

        cubes.append(Cube(x0, y0, z0, x1, y1, z1))

    cubes.sort()
    return cubes


def solution(filename: str) -> int:
    cubes: List[Cube] = parse(filename)

    for i in range(len(cubes)):
        cube: Cube = cubes[i]
        current_floor: int = 1

        for j in range(i - 1, -1, -1):
            other_cube: Cube = cubes[j]
            if cube.does_intersects(other_cube):
                current_floor = max(current_floor, other_cube.z1 + 1)

            cube.down_to(current_floor)

    cubes.sort()

    for i in range(len(cubes)):
        cube = cubes[i]
        for j in range(i - 1, -1, -1):
            other_cube = cubes[j]

            if cube.does_intersects(other_cube):
                # just on top
                if cube.z0 == other_cube.z1 + 1:
                    cube.supported_by(j)
                    other_cube.supports(i)

    crushed: int = 0
    for i, cube in enumerate(cubes):
        for j in cube.supports_list:
            if len(cubes[j].supported_by_list) <= 1:
                break
        else:
            crushed += 1

    return crushed


if __name__ == "__main__":
    print(solution("./example.txt"))  # 5
    print(solution("./input.txt"))  # 421
