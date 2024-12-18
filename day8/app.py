import itertools

f = open("day8/input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

size = (len(lines[0]), len(lines))
print(size)

# --- Part 1 ---

def in_bounds(x, y):
    return 0 <= x < size[0] and 0 <= y < size[1]

locations = {}
for i, line in enumerate(lines):
    for j, char in enumerate(line):
        if char != ".":
            if locations.get(char) is None:
                locations[char] = [(j, i)]
            else:
                locations[char].append((j, i))

antinodes = set()
for frequency in locations.keys():
    for i in itertools.combinations(locations[frequency], 2):
        dy = i[0][1] - i[1][1]
        dx = i[0][0] - i[1][0]
        
        # Find antinodes
        a1 = (i[0][0] + dx, i[0][1] + dy)
        a2 = (i[1][0] - dx, i[1][1] - dy)
        
        if in_bounds(*a1):
            antinodes.add(a1)
        if in_bounds(*a2):
            antinodes.add(a2)
            
print(f"Part 1: {len(antinodes)}")

# --- Part 2 ---

antinodes = set()
for frequency in locations.keys():
    for i in itertools.combinations(locations[frequency], 2):
        dy = i[0][1] - i[1][1]
        dx = i[0][0] - i[1][0]
        
        # Find antinodes
        a1 = (i[0][0] + dx, i[0][1] + dy)
        a2 = (i[1][0] - dx, i[1][1] - dy)
        
        # Check forwards until reached end of grid
        while in_bounds(*a1):
            if lines[a1[1]][a1[0]] != frequency:
                antinodes.add(a1)
            a1 = (a1[0] + dx, a1[1] + dy)
        
        # Check backwards until reached end of grid
        while in_bounds(*a2):
            if lines[a2[1]][a2[0]] != frequency:
                antinodes.add(a2)
            a2 = (a2[0] - dx, a2[1] - dy)
    
    # Need to add each antenna location to antinodes too
    for i in locations[frequency]:
        antinodes.add(i)
            
print(f"Part 2: {len(antinodes)}")