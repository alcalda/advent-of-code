def read_content(filename: str) -> list[list[str]]:
    with open(filename, mode="r") as file:
        grid = [list(line.strip()) for line in file]
    return grid

def count_occurrences(string: str, word: str) -> int:
    count = 0
    start = 0
    while start < len(string):
        idx = ''.join(string).find(word, start)
        if idx == -1:
            break
        else:
            count += 1
            start = idx + 1
    return count

def transposed(grid: list[list[str]]) -> list[list[str]]:
    return list(map(list, zip(*grid)))

def diagonal_slices(matrix):
    slices = []
    rows, cols = len(matrix), len(matrix[0])
    # upper-left to lower-right
    for k in range(rows + cols - 1):
        slice_ = []
        for i in range(max(0, k - cols + 1), min(rows, k + 1)):
            j = k - i
            slice_.append(matrix[i][j])
        slices.append(slice_)
    # upper-right to lower-left
    for k in range(rows + cols - 1):
        slice_ = []
        for i in range(max(0, k - cols + 1), min(rows, k + 1)):
            j = cols - 1 - (k - i)
            slice_.append(matrix[i][j])
        slices.append(slice_)

    return slices

def search_horizontal(grid: list[list[str]], word: str) -> int:
    count = 0
    for row in grid:
        count += ''.join(row).count(word)
        count += ''.join(reversed(row)).count(word)
    return count

def search_vertical(grid: list[list[str]], word: str) -> int:
    count = 0
    for row in transposed(grid):
        count += ''.join(row).count(word)
        count += ''.join(reversed(row)).count(word)
    return count

def search_diagonal(grid: list[list[str]], word: str) -> int:
    count = 0
    for row in diagonal_slices(grid):
        count += ''.join(row).count(word)
        count += ''.join(reversed(row)).count(word)
    return count

def solve(filename: str) -> int:
    grid = read_content(filename)
    result = 0
    print(f"horizontal: {search_horizontal(grid, 'XMAS')}")
    print(f"vertical: {search_vertical(grid, 'XMAS')}")
    print(f"diagonal: {search_diagonal(grid, 'XMAS')}")
    result += search_horizontal(grid, 'XMAS')
    result += search_vertical(grid, 'XMAS')
    result += search_diagonal(grid, 'XMAS')
    return result

print(f"Example Result = {solve('example.txt')}")
print(f"Input Result = {solve('input.txt')}")