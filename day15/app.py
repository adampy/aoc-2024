f = open("day15/input.txt", "r")
grid, instructions = f.read().split("\n\n")
f.close()

grid = grid.split("\n")
instructions = instructions.replace("\n", "")

start = None
for y, line in enumerate(grid):
    for x, cell in enumerate(line):
        if cell == "@":
            start = (x, y)
        
if start is None:
    raise Exception("No start found")

# --- Part 1 ---

class Direction:
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"
    
def print_grid(grid):
    for line in grid:
        print(line)
    print()
    
def try_move(grid, x, y, instruction):
    potential_x, potential_y = x, y
    if instruction == Direction.UP:
        potential_y -= 1
    elif instruction == Direction.RIGHT:
        potential_x += 1
    elif instruction == Direction.DOWN:
        potential_y += 1
    elif instruction == Direction.LEFT:
        potential_x -= 1
        
    potential_char = grid[potential_y][potential_x]
    if potential_char == "#":
        return (x, y), grid
    elif potential_char == "O":
        moved_pos, moved_grid = try_move(grid, potential_x, potential_y, instruction)
        if moved_pos != (potential_x, potential_y):
            # Then we can move the object at char to potential_char
            char = grid[y][x]
            grid[y] = grid[y][:x] + "." + grid[y][x+1:]
            grid[potential_y] = grid[potential_y][:potential_x] + char + grid[potential_y][potential_x+1:]
            return (potential_x, potential_y), grid
    elif potential_char == ".":
        # Then we can move the object at char to potential_char
        char = grid[y][x]
        grid[y] = grid[y][:x] + "." + grid[y][x+1:]
        grid[potential_y] = grid[potential_y][:potential_x] + char + grid[potential_y][potential_x+1:]
        return (potential_x, potential_y), grid
    
    return (x, y), grid

def get_gps_score(grid):
    gps_score = 0
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == "O":
                gps_score += (100 * y + x)
    return gps_score

part1_grid = grid.copy()
pos = start
for instruction in instructions:
    pos, part1_grid = try_move(part1_grid, *pos, instruction)
print(f"Part 1: {get_gps_score(part1_grid)}")

# --- Part 2 ---
    
def new_try_move(grid, x, y, instruction):
    def can_push_box(box_x, box_y, instruction):
        # ASSUMES THAT BOX_X IS LEFT CHAR OF BOX, i.e. [
            
        # Boundary check
        dy = -1 if instruction == Direction.UP else 1
        if box_y + dy < 0 or box_y + dy >= len(grid) or grid[box_y+dy][box_x] == "#" or grid[box_y+dy][box_x+1] == "#":
            return False
        
        # If boxes are above, pushing this box is the same as being able to push each of the above boxes
        can_push_this_box = True
        for dx in range(-1, 2):
            if grid[box_y+dy][box_x+dx] == "[":
                can_push_this_box = can_push_this_box and can_push_box(box_x+dx, box_y+dy, instruction)
                
        return can_push_this_box
    
    def push_box(grid, box_x, box_y, instruction):
        # Push any aboveboxe either up or down
        dy = -1 if instruction == Direction.UP else 1
        for dx in range(-1, 2):
            if grid[box_y+dy][box_x+dx] == "[":
                grid = push_box(grid, box_x+dx, box_y+dy, instruction)
        
        # Move box
        grid[box_y+dy] = grid[box_y+dy][:box_x] + "[]" + grid[box_y+dy][box_x+2:]
        # Set old postion to empty
        grid[box_y] = grid[box_y][:box_x] + ".." + grid[box_y][box_x+2:]
        return grid
    
    potential_x, potential_y = x, y
    if instruction == Direction.UP:
        potential_y -= 1
    elif instruction == Direction.RIGHT:
        potential_x += 1
    elif instruction == Direction.DOWN:
        potential_y += 1
    elif instruction == Direction.LEFT:
        potential_x -= 1
        
    potential_char = grid[potential_y][potential_x]
    if potential_char == "#":
        return (x, y), grid
    elif potential_char == "[" or potential_char == "]":
        # Then we are pushing boxes either horizontally (in 'if' case below) or vertically (in 'else' case)
        if instruction == Direction.LEFT or instruction == Direction.RIGHT:
            moved_pos, moved_grid = new_try_move(grid, potential_x, potential_y, instruction)
            if moved_pos != (potential_x, potential_y):
                # Then we can move the object at char to potential_char
                char = grid[y][x]
                grid[y] = grid[y][:x] + "." + grid[y][x+1:]
                grid[potential_y] = grid[potential_y][:potential_x] + char + grid[potential_y][potential_x+1:]
                return (potential_x, potential_y), grid
        else:
            # If pushing vertically up, we need to check that all horizontal cells of boxes can also be pushed
            box_above_x = potential_x if potential_char == "[" else potential_x-1 # x pos of box directly above
            can_push = can_push_box(box_above_x, potential_y, instruction)
            
            if can_push:
                # Then we need to move all [ and ] chars in direction of instruction
                grid = push_box(grid, box_above_x, potential_y, instruction)
                
                # Then we need to move robot in direction of instruction
                char = grid[y][x]
                grid[y] = grid[y][:x] + "." + grid[y][x+1:]
                grid[potential_y] = grid[potential_y][:potential_x] + char + grid[potential_y][potential_x+1:]
                return (potential_x, potential_y), grid
            
            # Cannot push, return current position
            return (x, y), grid
        
    elif potential_char == ".":
        # Then we can move the object at char to potential_char
        char = grid[y][x]
        grid[y] = grid[y][:x] + "." + grid[y][x+1:]
        grid[potential_y] = grid[potential_y][:potential_x] + char + grid[potential_y][potential_x+1:]
        return (potential_x, potential_y), grid
    
    return (x, y), grid

def new_get_gps_score(grid):
    gps_score = 0
    for y, line in enumerate(grid):
        for x, cell in enumerate(line):
            if cell == "[":
                gps_score += (100 * y + x)
    
    # Firstly check left half of map
    # for y, line in enumerate(grid):
    #     for x in range(len(line)//2):
    #         if grid[y][x] == "[":
    #             gps_score += (100 * y + x)
                
    # # Then check right half of map
    # for y, line in enumerate(grid):
    #     for x in range(len(line)//2, len(line)):
    #         if grid[y][x] == "]":
    #             gps_score += (100 * y + x)
    
    return gps_score

# Make a new expanded grid
expanded_grid = []
for y, line in enumerate(grid):
    expanded_line = ""
    for x, cell in enumerate(line):
        if cell == "@":
            expanded_line += "@."
        elif cell == "O":
            expanded_line += "[]"
        elif cell == "#":
            expanded_line += "##"
        else:
            expanded_line += ".."
    expanded_grid.append(expanded_line)
    
# Run instructions
# pos = start
# for instruction in instructions:
#     pos, expanded_grid = new_try_move(expanded_grid, *pos, instruction)
# print(f"Part 2: {new_get_gps_score(expanded_grid)}")

# Find start point
start = None
for y, line in enumerate(expanded_grid):
    for x, cell in enumerate(line):
        if cell == "@":
            start = (x, y)
            break
if start is None:
    raise Exception("No start found")
    
pos = start
for instruction in instructions:
    pos, expanded_grid = new_try_move(expanded_grid, *pos, instruction)
print_grid(expanded_grid)
print(f"Part 2: {new_get_gps_score(expanded_grid)}")

# print_grid(expanded_grid)
# pos, expanded_grid = new_try_move(expanded_grid, *start, Direction.LEFT)
# print_grid(expanded_grid)

# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.DOWN)
# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.DOWN)
# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.LEFT)
# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.LEFT)
# print_grid(expanded_grid)

# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.UP)
# print_grid(expanded_grid)

# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.UP)
# print_grid(expanded_grid)

# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.LEFT)
# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.LEFT)
# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.UP)
# print_grid(expanded_grid)

# pos, expanded_grid = new_try_move(expanded_grid, *pos, Direction.UP)
# print_grid(expanded_grid)