import re

def add(f: int, g: int) -> int:
    return f * g

def solve(filename: str) -> int:
    mul = r"(?:mul\()(\d+)(?:,)(\d+)(?:\))"
    do = r"do\(\)"
    dont = r"don't\(\)"
    all = re.compile(f"({mul}|{do}|{dont})")
    with open(filename, mode="r") as file:
        matches = re.findall(all, file.read())
        result : int = 0
        enabled = True
        for match in matches:
            if match[0].startswith("mul"):
                if enabled:
                    result += add(int(match[1]), int(match[2]))
            elif match[0].startswith("do()"):
                enabled = True
            elif match[0].startswith("don't()"):
                enabled = False
        return result


print(f"Safe Example = {solve('example2.txt')}")
print(f"Safe Reports = {solve('input.txt')}")