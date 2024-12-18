f = open("day12/input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()

# --- Part 1 ---

class Region:
    def __init__(self, x, y, char):
        self.coordinates = set()
        self.coordinates.add((x, y))
        self.char = char
        self.perimeter = 4
        
    def __str__(self):
        return f"Region {self.char} with area {len(self.coordinates)}, perimeter {self.perimeter}, and coordinates\n\t{self.coordinates}"

    def calculate_perimeter(self):
        if len(self.coordinates) == 1:
            return 4
        
        # Add the base perimeter contribution of all coordinates in the region
        perim_contribs = {}
        for x, y in self.coordinates:
            perim_contribs[(x, y)] = 4
        
        # Now modify each contrib, by subtracting the number of neighbours present
        for x, y in self.coordinates:
            for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                p = (x + dx, y + dy)
                if p in self.coordinates:
                    perim_contribs[p] -= 1
        
        return sum(perim_contribs.values())
    
    def calculate_sides(self):
        def num_corners(x, y) -> int:
            corners = 0
            
            left = (x - 1, y) in self.coordinates
            right = (x + 1, y) in self.coordinates
            up = (x, y - 1) in self.coordinates
            down = (x, y + 1) in self.coordinates
            lower_left = (x - 1, y + 1) in self.coordinates
            lower_right = (x + 1, y + 1) in self.coordinates
            upper_right = (x + 1, y - 1) in self.coordinates
            upper_left = (x - 1, y - 1) in self.coordinates
            
            # Check for upper left outer corner
            if not left and not up:
                corners += 1
            # Check for upper right outer corner
            if not right and not up:
                corners += 1
            # Check for lower right outer corner
            if not right and not down:
                corners += 1
            # Check for lower left outer corner
            if not left and not down:
                corners += 1
            
            # Check for upper left inner corner
            if right and down and not lower_right:
                corners += 1
            # Check for upper right inner corner
            if left and down and not lower_left:
                corners += 1
            # Check for lower right inner corner
            if left and up and not upper_left:
                corners += 1
            # Check for lower left inner corner
            if right and up and not upper_right:
                corners += 1
            
            return corners
        
        # Number of sides is equal to the number of corners
        # Must count inner corners as well as outer corners
        corners = 0
        for x, y in self.coordinates:
            corners += num_corners(x, y)
        return corners
            

regions = []
def get_existing_region(x, y, char) -> Region | None:
    for region in regions:
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            p = (x + dx, y + dy)
            if p in region.coordinates and region.char == char:
                return region
    return None

print("Processing regions...")
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        p = (x, y)
        region = get_existing_region(x, y, char)
        if region is None:
            regions.append(Region(x, y, char))
        else:
            region.coordinates.add(p)
   

# Coalesce regions
print("Coalescing regions...")
i = len(regions) - 1
while i > 0:
    print(f"\t{len(regions) - i}/{len(regions) - 1}")
    region = regions[i]
    for coordinate in region.coordinates:
        existing = get_existing_region(coordinate[0], coordinate[1], region.char)
        if existing is not None and existing != region:
            existing.coordinates.update(region.coordinates)
            regions.pop(i)
            break
    i -= 1

print("Calculating total price...")
total_price = 0
for region in regions:
    area = len(region.coordinates)
    perimeter = region.calculate_perimeter()
    
    total_price += area * perimeter
print(f"Part 1: {total_price}")

# --- Part 2 ---
total_price = 0
for region in regions:
    area = len(region.coordinates)
    sides = region.calculate_sides()
    
    total_price += area * sides
print(f"Part 2: {total_price}")
