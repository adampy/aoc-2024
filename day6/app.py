# Find start pos and orientation
class Orientation:
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"
OBSTACLE = "#"

def get_grid():
    f = open("day6/input.txt", "r")
    lines = [l.strip() for l in f.readlines()]
    f.close()
    return lines

def get_start_pos_and_orientation(lines):
    x_pos = 0
    y_pos = 0
    orientation = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c in [Orientation.UP, Orientation.RIGHT, Orientation.DOWN, Orientation.LEFT]:
                x_pos = x
                y_pos = y
                orientation = c
    return x_pos, y_pos, orientation
    
def next_orientation(orientation):
    if orientation == Orientation.UP:
        return Orientation.RIGHT
    elif orientation == Orientation.RIGHT:
        return Orientation.DOWN
    elif orientation == Orientation.DOWN:
        return Orientation.LEFT
    elif orientation == Orientation.LEFT:
        return Orientation.UP
    return None
    
def turn_right_until_no_obstacle(x, y, orientation, lines):
    seen_obstacles = set()
    while (True):
        ahead = move_forward(x, y, orientation)
        if not in_bounds(ahead[0], ahead[1], lines):
            break
        if lines[ahead[1]][ahead[0]] == OBSTACLE:
            seen_obstacles.add(ahead)
            orientation = next_orientation(orientation)
        else:
            break
    return orientation, seen_obstacles

def move_forward(x, y, orientation):
    if orientation == Orientation.UP:
        return x, y - 1
    elif orientation == Orientation.RIGHT:
        return x + 1, y
    elif orientation == Orientation.DOWN:
        return x, y + 1
    elif orientation == Orientation.LEFT:
        return x - 1, y
    return 0, 0

def in_bounds(x, y, lines):
    return x >= 0 and x < len(lines[0]) and y >= 0 and y < len(lines)

def is_seen_obstacle_ahead(x, y, orientation, lines):
    while (True):
        x, y = move_forward(x, y, orientation)
        if not in_bounds(x, y, lines):
            return False
        if lines[y][x] == OBSTACLE and (x, y) in seen_obstacles: #(prev_x, prev_y) in turning_points:
            return True


if __name__ == "__main__":
    # --- Part 1 ---
    lines = get_grid()
    
    x_pos, y_pos, orientation = get_start_pos_and_orientation(lines)
    start_pos = (x_pos, y_pos)
    start_orientation = orientation

    positions = set()
    positions.add(start_pos)

    while (True):
        orientation, _ = turn_right_until_no_obstacle(x_pos, y_pos, orientation, lines)
        x_pos, y_pos = move_forward(x_pos, y_pos, orientation)
            
        if not in_bounds(x_pos, y_pos, lines):
            break
        
        positions.add((x_pos, y_pos))

    print(f"Part 1: {len(positions)}")
    
    # --- Part 2 ---
    
    x_pos = start_pos[0]
    y_pos = start_pos[1]
    orientation = start_orientation

    turning_points = set()
    seen_obstacles = set()
    new_obstacles = set()

    while (True):
        # Check if we can place obstacle s.t. if we turn right we have already been there
        right = next_orientation(orientation)
        if is_seen_obstacle_ahead(x_pos, y_pos, right, lines):
            new_obs = move_forward(x_pos, y_pos, orientation)
            if new_obs[0] != start_pos[0] or new_obs[1] != start_pos[1]:  
                new_obstacles.add(new_obs)
        
        # Keep track of where we turn, i.e. there is an obstacle in front of us
        before_orientation = orientation
        orientation, obstacles = turn_right_until_no_obstacle(x_pos, y_pos, orientation, lines)
        seen_obstacles.update(obstacles)
        if orientation != before_orientation:
            turning_points.add((x_pos, y_pos))
            
        x_pos, y_pos = move_forward(x_pos, y_pos, orientation)
            
        if not in_bounds(x_pos, y_pos, lines):
            break
        
    print(f"Part 2: {len(new_obstacles)}")