f = open("day4/input.txt", "r")
lines = f.readlines()
f.close()
lines = [line.strip() for line in lines]


# --- Part 1 ---

def search_pos(row, col) -> int:    
    # Initialise increments
    incs = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]
    
    # Iterate through search_word in each direction
    total_found = 0
    for inc in incs:
        
        # Scan in direction for search_word
        is_found = True
        row_to_check = row
        col_to_check = col
        for i, char in enumerate(SEARCH_WORD):
            row_to_check = row + i * inc[0]
            col_to_check = col + i * inc[1]
            
            if row_to_check < 0 or row_to_check >= len(lines) or col_to_check < 0 or col_to_check >= len(lines[row_to_check]) \
                or lines[row_to_check][col_to_check] != char:
                is_found = False
                break # Break out of searching word to check next direction
        
        # If found, add to total
        if is_found:
            total_found += 1
            
    return total_found

SEARCH_WORD = "XMAS"
found = 0
for row in range(len(lines)):
    for col in range(len(lines[row])):        
        found += search_pos(row, col)
        
print(f"Part1: {found}")

# --- Part 2 ---

def search_pos_part2(row, col) -> int:
    total_found = 0
    
    def in_grid(row, col):
        return row >= 0 and row < len(lines) and col >= 0 and col < len(lines[row])
    def grid_char(row, col):
        return lines[row][col] if in_grid(row, col) else None
    
    # Only check from A
    if grid_char(row, col) != 'A':
        return 0
    
    # Top left to bottom right direction
    top_left = (grid_char(row - 1, col - 1) == 'M' and grid_char(row + 1, col + 1) == 'S') \
        or (grid_char(row - 1, col - 1) == 'S' and grid_char(row + 1, col + 1) == 'M')
    
    # Top right to bottom left direction
    top_right = (grid_char(row - 1, col + 1) == 'M' and grid_char(row + 1, col - 1) == 'S') \
        or (grid_char(row - 1, col + 1) == 'S' and grid_char(row + 1, col - 1) == 'M')
    
    return 1 if top_left and top_right else 0
    

found = 0
for row in range(len(lines)):
    for col in range(len(lines[row])):        
        found += search_pos_part2(row, col)
        
print(f"Part2: {found}")