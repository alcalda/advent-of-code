def read_content(filename: str) -> list[list[str]]:
    with open(filename, mode="r") as file:
        grid = [list(line.strip()) for line in file]
    return grid

def find_diagonal_substrings(grid, substring):
    def search_direction(x, y, dx, dy):
        positions = []
        for i in range(len(substring)):
            if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
                return []
            if grid[x][y] != substring[i]:
                return []
            positions.append((x, y))
            x += dx
            y += dy
        return positions

    diagonals = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            for dx, dy in directions:
                positions = search_direction(i, j, dx, dy)
                if positions:
                    diagonals.append(positions)
    return diagonals

def find_crossings(diagonals):
    crossings = 0
    for i in range(len(diagonals)):
        for j in range(i + 1, len(diagonals)):
            a1 = diagonals[i][1]
            a2 = diagonals[j][1]
            if a1 == a2:
                crossings += 1
    return crossings

def solve(filename: str) -> int:
    grid = read_content(filename)
    diagonals = find_diagonal_substrings(grid, 'MAS')
    result = find_crossings(diagonals)
    return result

print(f"Example Result = {solve('example.txt')}")
print(f"Input Result = {solve('input.txt')}")