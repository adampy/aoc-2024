from day16utils import dijkstras, print_route

f = open("day18/input.txt", "r")
blocks = []
for line in f.readlines():
    x, y = line.strip().split(",")
    blocks.append((int(x), int(y)))
lines = [line.strip() for line in f.readlines()]
f.close()

# --- Part 1 ---

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print()
    
def simulate(grid, blocks, part1=False):
    for block in blocks:
        grid[block[1]][block[0]] = "#"
    #print_grid(grid)
    
    # Now run dijkstras on new grid
    shortest_dist, completed_routes = dijkstras(grid, start, end)
    if shortest_dist is None or completed_routes is None:
        if part1:
            print("Part 1: No route found")
        return False
    
    if part1:
        print("Part 1:", shortest_dist)
        #print_route(grid, completed_routes[-1][0], start, end)
    return True
    
    
# Simulate first N blocks

N = 1024
WIDTH = 71
HEIGHT = 71

start = (0, 0)
end = (WIDTH - 1, HEIGHT - 1)
grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

simulate(grid, blocks[:N], True)

# --- Part 2 ---

# Simulate all blocks and find first that breaks
for n in range(N + 1, len(blocks)):
    if not simulate(grid, blocks[:n]):
        broken = blocks[n-1]
        print(f"Part 2: {broken[0]},{broken[1]}")
        break