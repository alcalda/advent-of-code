import itertools
from collections import defaultdict
from typing import Protocol


class AoCProtocol(Protocol):
    def read_content(self, filename: str):
        ...

    def solve(self) -> int:
        ...

class GuardGallivant(AoCProtocol):
    obstacles: set[tuple[int, int]] = set()
    positions: set[tuple[int, int]] = set()
    movements: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    guard: tuple[int, int]
    maxX: int = 0
    maxY: int = 0
    moves: int = 0
    loop: bool = False
    start: tuple[int, int] = None
    cyclic_iterator: itertools.cycle
    step = None


    # four turns (x,y)
    steps = (
        (0, -1),  # up
        (1, 0),  # right
        (0, 1),  # down
        (-1, 0),  # left
    )

    @classmethod
    def from_file(cls, filename: str):
        return cls(filename)

    def reset(self):
        self.cyclic_iterator = itertools.cycle(GuardGallivant.steps)
        self.step = next(self.cyclic_iterator)
        self.positions.clear()
        self.movements.clear()
        self.moves = 0
        self.guard = self.start
        self.loop = False

    def __init__(self, filename: str):
        self.reset()
        self.obstacles.clear()
        self.start = None
        self.read_content(filename)

    def read_content(self, filename: str):
        with open(filename, mode="r") as file:
            for lineno, line in enumerate(file):
                self.maxX = len(line.strip()) - 1
                self.maxY = lineno
                obs = {(pos, lineno) for pos, c in enumerate(line) if c == "#"}
                self.obstacles |= obs
                if line.count("^"):
                    self.guard = (line.index("^"), lineno)
                    self.start = self.guard
                    self.positions = {self.guard}

    def obstructed(self) -> bool:
        return tuple(map(lambda x, y: x + y, self.guard, self.step)) in self.obstacles

    def onmap(self) -> bool:
        if not (0 <= self.guard[0] <= self.maxX):
            return False
        if not (0 <= self.guard[1] <= self.maxY):
            return False
        else:
            return True

    def move(self) -> tuple[int, int]:
        self.guard = tuple(map(lambda x, y: x + y, self.guard, self.step))
        return self.guard

    def patrol(self):
        if self.obstructed():
            self.step = next(self.cyclic_iterator)
        if self.step in self.movements[self.guard]:
            self.loop = True
        if not self.loop:
            self.movements[self.guard].add(self.step)
            self.positions.add(self.move())
            self.moves += 1

    def solve(self) -> int:
        while self.onmap():
            self.patrol()
        # remove the position outside the map
        self.positions.remove(self.guard)
        # print(f"{self.moves=} == {sum(len(v) for v in self.movements.values())}")
        return len(self.positions)

    def obstruct(self) -> int:
        result: set[tuple[int, int]] = set()
        for obstruction in itertools.product(range(self.maxX + 1), range(self.maxY + 1)):
            if obstruction not in self.obstacles:
                self.reset()
                self.obstacles.add(obstruction)
                while (not self.loop) and self.onmap():
                    self.patrol()
                self.obstacles.remove(obstruction)
                if self.loop:
                    result.add(obstruction)
        return len(result)


guard1 = GuardGallivant.from_file("example.txt")
# print(f"Example: {guard1.solve()} with {guard1.moves=}")
guard2 = GuardGallivant.from_file("input.txt")
# print(f"Input: {guard2.solve()} with {guard2.moves=}")

guard1 = GuardGallivant.from_file("example.txt")
# print(f"Example: {guard1.obstruct()}")
guard2 = GuardGallivant.from_file("input.txt")
print(f"Input: {guard2.obstruct()}")
