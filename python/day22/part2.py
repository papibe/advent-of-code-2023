import re
from collections import deque
from copy import deepcopy
from typing import Deque, List, Match, Optional, Set, Tuple


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
        upper_cube = cubes[i]
        current_floor: int = 1

        for j in range(i - 1, -1, -1):
            lower_cube = cubes[j]
            if upper_cube.does_intersects(lower_cube):
                current_floor = max(current_floor, lower_cube.z1 + 1)

            upper_cube.down_to(current_floor)

    cubes.sort()

    for upper_index in range(len(cubes)):
        upper_cube = cubes[upper_index]
        for lower_index in range(upper_index - 1, -1, -1):
            lower_cube = cubes[lower_index]

            if upper_cube.does_intersects(lower_cube):
                # just on top
                if upper_cube.z0 == lower_cube.z1 + 1:
                    upper_cube.supported_by(lower_index)
                    lower_cube.supports(upper_index)

    total_fallen: int = 0

    for lower_index in range(len(cubes)):
        new_cubes: List[Cube] = deepcopy(cubes)
        lower_cube = new_cubes[lower_index]

        queue: Deque[Tuple[int, Cube]] = deque([(lower_index, lower_cube)])
        visited: Set[Cube] = set([lower_cube])

        while queue:
            lower_index, lower_cube = queue.popleft()
            affected: List[Tuple[int, Cube]] = []
            for upper_index in lower_cube.supports_list:
                upper_cube = new_cubes[upper_index]
                supported: List[int] = upper_cube.supported_by_list
                if lower_index in supported:
                    supported.remove(lower_index)

                    affected.append((upper_index, upper_cube))

            for index, affected_cube in affected:
                if affected_cube in visited:
                    continue
                if not affected_cube.supported_by_list:
                    queue.append((index, affected_cube))
                    visited.add(affected_cube)

        local_fallen: int = 0
        for cube in new_cubes:
            if len(cube.supported_by_list) == 0 and cube.z0 != 1:
                local_fallen += 1
        total_fallen += local_fallen

    return total_fallen


if __name__ == "__main__":
    print(solution("./example.txt"))  # 7
    print(solution("./input.txt"))  # 39247
