import re

def add(f: int, g: int) -> int:
    return f * g

def solve(filename: str) -> int:
    pattern = r"(?:mul\()(\d+)(?:,)(\d+)(?:\))"
    with open(filename, mode="r") as file:
        matches = re.findall(pattern, file.read())
        for match in matches:
            pass
        result = sum(map(lambda f: int(f[0]) * int(f[1]), matches))
        return result



print(f"Example Result = {solve('example.txt')}")
print(f"Input Result = {solve('input.txt')}")