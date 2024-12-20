from day18utils import *

f = open("day20/input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

# --- Part 1 ---
    
# Find the start and end position
start = (0, 0)
end = (0, 0)
for i, line in enumerate(lines):
    if "S" in line:
        start = (line.index("S"), i)
    if "E" in line:
        end = (line.index("E"), i)
        
res = dijkstras(lines, start, end)
assert res[0] is not None, "No path found"
assert res[1] is not None, "No path found"
path = res[1][0][0]

path_index_map = {} # holds the index of the position in the path
for i, (p1, p2) in enumerate(path):
    path_index_map[(p1, p2)] = i

def get_saving(start, end) -> int:
    return path_index_map[end] - path_index_map[start]

def distance(p1, p2) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_cheats(grid, path, up_to=20) -> int:
    cheat_set = set() # set of ((x1, y1), (x2, y2)) of cheat (start position, end position)
    
    for p in path:
        for dx in range(-up_to, up_to + 1):
            for dy in range(-up_to, up_to + 1):
                nx = p[0] + dx
                ny = p[1] + dy
                if nx == p[0] and ny == p[1]:
                    continue
                if nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid):
                    continue
                if distance(p, (nx, ny)) > up_to:
                    continue
                
                if grid[ny][nx] == "#":
                    continue
                
                if ((nx, ny), p) not in cheat_set:
                    cheat_set.add((p, (nx, ny)))
    
    count = 0
    for p1, p2 in cheat_set:
        saving = get_saving(p1, p2) - distance(p1, p2) + 1 # + cheat distance
        
        if saving >= 100:
            count += 1
    return count

# --- Part 1 and Part 2 ---
print(f"Part 1: {get_cheats(lines, path, 2)}")
print(f"Part 2: {get_cheats(lines, path, 20)}")