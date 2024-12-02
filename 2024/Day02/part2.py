from itertools import pairwise

def deviation(pair: tuple) -> int:
    return pair[1] - pair[0]

def is_safe(levels: list[int]) -> bool:
    deviations = list(map(deviation, pairwise(levels)))
    if all(-1 >= x >= -3 for x in deviations):
        return True
    if all(1 <= x <= 3 for x in deviations):
        return True

def is_safe_dampened(levels: list[int]) -> bool:
    for i in range(len(levels)):
        damp = levels[:i] + levels[i+1:]
        if is_safe(damp):
            return True
    return False

def solve(filename: str) -> int:
    count: int = 0
    with open(filename, mode="r") as file:
        for report in file:
            levels = list(map(int, report.split()))
            count += 1 if is_safe_dampened(levels) else 0
    return count

print(f"Safe Dampened Example = {solve('example.txt')}")
print(f"Safe Dampened Reports = {solve('input.txt')}")
