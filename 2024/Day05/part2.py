import itertools
from collections import defaultdict


def parse_rules(filename: str):
    with open(filename, mode="r") as file:
        return file.read()

def read_content(filename: str):
    rules: list = []
    updates: list = []
    with open(filename, mode="r") as file:
        for line in file:
            if line.count("|"):
                rules.append(list(map(int, line.strip().split("|"))))
            elif line.count(","):
                updates.append(list(map(int, line.strip().split(","))))
    return rules, updates

def sort_rules(rules: list) -> dict:
    graph = defaultdict(list)
    for before, after in rules:
        graph[before].append(after)
    return graph

def middle(nums: list) -> int:
    middle = int((len(nums) - 1) / 2)
    return nums[middle]

def sort(update: list, graph: defaultdict):
    sorted: list = update[:]

    for (idx, page) in enumerate(update):
        if idx < len(update) - 1 and page in graph:
            if update[idx + 1] not in graph[page]:
                sorted[idx], sorted[idx + 1] = sorted[idx + 1], sorted[idx]
    update = sorted

def sort_updates(rules: list, updates: list) -> int:
    result: int = 0
    order_rules = sort_rules(rules)
    indexes: list = []
    for (idx, update) in enumerate(updates):
        no_dependencies = [page for page in update if page not in [n for rule in order_rules.values() for n in rule]]
        # Initialize the sorted list
        sorted_numbers = []

        # Perform sorting
        while no_dependencies:
            num = no_dependencies.pop(0)
            sorted_numbers.append(num)
            if num in order_rules:
                for dependent in order_rules[num]:
                    if dependent not in sorted_numbers and all(prereq in sorted_numbers for prereq in
                                                               [k for k, v in order_rules.items() if dependent in v]):
                        no_dependencies.append(dependent)

        for before, after in itertools.pairwise(update):
            if after not in order_rules[before]:
                sort(update, order_rules)
                indexes.append(idx)

        #     before = update[i]
        #     after = update[j]
        #     if after not in graph[before] and before in graph[after]:
        #         update[i], update[j] = update[j], update[i]
        #         invalid = True
        #     i += 1
        #     j += 1
        # if invalid:
        #     indexes.append(idx)
    for idx in indexes:
        result += updates[idx]
    return result

def solve(filename: str) -> int:
    rules, updates = read_content(filename)
    result = sort_updates(rules, updates)
    return result

print(f"Example Result = {solve('example.txt')}")
print(f"Input Result = {solve('input.txt')}")