def distance(a, b) -> int:
    distance = abs(a - b)
    # print(f"{a=}, {b=}, {distance=}")
    return distance


def solve(filename: str) -> int:
    with open(filename, mode="r") as file:
        list1, list2 = zip(*(line.split() for line in file))
        list1, list2 = (list(map(int, sorted(list1))), list(map(int, sorted(list2))))
    distances = map(distance, list1, list2)
    result = sum(distances)
    return result


print(f"Overall Distance = {solve('input.txt')}")
