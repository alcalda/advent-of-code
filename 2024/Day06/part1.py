import itertools
from collections import defaultdict
from typing import Protocol
import copy

class AoCProtocol(Protocol):
    def read_content(self, filename: str):
        ...

    def solve(self) -> int:
        ...

class GuardGallivant(AoCProtocol):
    # four turns (x,y)
    steps = (
        (0, -1),  # up
        (1, 0),  # right
        (0, 1),  # down
        (-1, 0),  # left
    )

    Position = tuple[int, int]
    Direction = tuple[int, int]
    PositionDirection = tuple[Position, Direction]

    @classmethod
    def from_file(cls, filename: str):
        return cls(filename)

    def __init__(self, filename: str):
        self.obstacles: set[GuardGallivant.Position] = set()
        self.positions: set[GuardGallivant.Position] = set()
        self.visited: set[GuardGallivant.PositionDirection] = set()
        self.maxX: int = 0
        self.maxY: int = 0
        self.moves: int = 0
        self.loop: bool = False
        self.start: GuardGallivant.Position = None
        self.guard: GuardGallivant.Position = None
        self.cyclic_iterator = itertools.cycle(GuardGallivant.steps)
        self.step: GuardGallivant.Direction = next(self.cyclic_iterator)
        self.reset()
        self.read_content(filename)

    def reset(self):
        self.cyclic_iterator = itertools.cycle(GuardGallivant.steps)
        self.step = next(self.cyclic_iterator)
        self.visited.clear()
        self.moves = 0
        self.guard = self.start
        self.loop = False

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

    def peek(self) -> Position:
        return tuple(map(lambda x, y: x + y, self.guard, self.step))

    def move(self) -> tuple[int, int]:
        self.guard = self.peek()
        return self.guard

    def obstructed(self) -> bool:
        return self.peek() in self.obstacles

    def onmap(self) -> bool:
        if not (0 <= self.guard[0] <= self.maxX):
            return False
        if not (0 <= self.guard[1] <= self.maxY):
            return False
        else:
            return True

    def patrol(self):
        if self.obstructed():
            posdir = GuardGallivant.PositionDirection((self.peek(), self.step))
            if posdir in self.visited:
                self.loop = True
                return
            self.visited.add(posdir)
            self.step = next(self.cyclic_iterator)
        else:
        # if not self.loop:
            self.positions.add(self.move())
            self.moves += 1

    def solve(self) -> int:
        while self.onmap():
            self.patrol()
        # remove the position outside the map
        self.positions.remove(self.guard)
        return len(self.positions)

    def obstruct(self) -> int:
        result: set[tuple[int, int]] = set()
        left: int = 0
        known = copy.copy(self.positions)
        for idx, obstruction in enumerate(known):
            self.reset()
            self.obstacles.add(obstruction)
            while (not self.loop) and self.onmap():
                self.patrol()
            self.obstacles.remove(obstruction)
            if self.loop:
                result.add(obstruction)
            if not self.onmap():
                left += 1
            # print(f"{idx}/{len(known)} with {self.moves=}|{self.loop=}, {self.onmap()=}")
        print(f"{left=} | {len(result)=}")
        return len(result)


guard1 = GuardGallivant.from_file("example.txt")
print(f"Example: {guard1.solve()} with {guard1.moves=}")
guard2 = GuardGallivant.from_file("input.txt")
print(f"Input: {guard2.solve()} with {guard2.moves=}")

print(f"Example: {guard1.obstruct()}")
print(f"Input: {guard2.obstruct()}")
