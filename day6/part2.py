# Adapted from: https://github.com/francescopeluso/AOC24/blob/main/day6/main.py

from app import * 

lines = get_grid()
x_pos, y_pos, orientation = get_start_pos_and_orientation(lines)

def causes_loop(x, y, orientation, lines):
    visited = set()
    while (True):
        orientation, _ = turn_right_until_no_obstacle(x, y, orientation, lines)
        x, y = move_forward(x, y, orientation)
        
        if (x, y, orientation) in visited:
            return True
        if not in_bounds(x, y, lines):
            return False
        visited.add((x, y, orientation))

num_obstacles = 0
for y in range(len(lines)):
    for x in range(len(lines[y])):
        if (x_pos == x and y_pos == y) or lines[y][x] == OBSTACLE:
            continue
        
        lines_copy = [list(line) for line in lines]
        lines_copy[y][x] = OBSTACLE
        if causes_loop(x_pos, y_pos, orientation, lines_copy):
            num_obstacles += 1
            
print(f"Part 2: {num_obstacles}")
        