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

def filter_updates(rules: list, updates: list) -> int:
    result: int = 0
    graph = sort_rules(rules)
    indexes: list = []
    for (idx, update) in enumerate(updates):
        invalid = False
        for pair in itertools.pairwise(update):
            if pair[1] not in graph[pair[0]]:
                invalid = True
        if not invalid:
            indexes.append(idx)
    for idx in indexes:
        middle = int((len(updates[idx]) - 1) / 2)
        result += updates[idx][middle]
    return result

def solve(filename: str) -> int:
    rules, updates = read_content(filename)
    result = filter_updates(rules, updates)
    return result

print(f"Example Result = {solve('example.txt')}")
print(f"Input Result = {solve('input.txt')}")