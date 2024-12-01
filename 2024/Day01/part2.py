from collections import Counter


def solve(filename: str) -> int:
    with open(filename, mode="r") as file:
        list1, list2 = zip(*(line.split() for line in file))
        list1, list2 = (list(map(int, list1)), list(map(int, list2)))
    result: int = sum(num * Counter(list2)[num] for num in list1)
    return result


print(f"Resemblance = {solve('input.txt')}")
