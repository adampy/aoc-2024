f = open("day16/input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

# --- Part 1 ---

# Find the start and end position
start = (0, 0)
end = (0, 0)
dots = 0
for i, line in enumerate(lines):
    if "S" in line:
        start = (line.index("S"), i)
    if "E" in line:
        end = (line.index("E"), i)
    dots += line.count(".")
#print(4*dots)

class Direction:
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (1, 0)
    WEST = (-1, 0)

completed_routes = []
fringe = [(start, [start], 0, Direction.EAST)]

visited = {}

while fringe:
    u, path, distance, direction = fringe.pop(0)
    
    if distance > 107468:
        continue
    
    # Check if we have reached the end
    if u == end:
        completed_routes.append((path + [end], distance, direction))
        continue
    
    visited[(u, direction)] = distance
    
    for dir in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
        potential = (u[0] + dir[0], u[1] + dir[1])
        
        # Out of bounds check
        if not (0 <= potential[0] < len(lines) and 0 <= potential[1] < len(lines[0])):
            continue
        
        # Wall check
        char = lines[potential[1]][potential[0]]
        if char == "#":
            continue
        
        if potential in path:
            continue
        
        # Already visited check
        if (potential, dir) in visited and visited[(potential, dir)] < distance:
            continue
        
        visited[(potential, dir)] = distance + 1 if dir == direction else distance + 1001
        
        if dir == direction:
            # Continue in the same direction
            fringe.append((potential, path + [u], distance + 1, dir))
        else:
            # Change direction
            fringe.append((potential, path + [u], distance + 1001, dir))
            
shortest_dist = completed_routes[-1][1]
print(f"Part 1: {shortest_dist}")

# --- Part 2 ---
tiles_on_best_paths = set()
for path, distance, direction in completed_routes:
    # Only include paths with the shortest distance
    if distance != shortest_dist:
        continue
    
    for tile in path:
        tiles_on_best_paths.add(tile)
        
# for y in range(len(lines)):
#     for x in range(len(lines[0])):
#         if (x, y) in tiles_on_best_paths:
#             print("O", end="")
#         else:
#             print(lines[y][x], end="")
#     print()
        
print(f"Part 2: {len(tiles_on_best_paths)}")

# for path, distance, direction in completed_routes:
#     print(f"{path, distance}\n")