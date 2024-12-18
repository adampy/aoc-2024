f = open("day5/input.txt", "r")
lines = f.readlines()
f.close()
lines = [line.strip() for line in lines]

rules = []
updates = []
reached_middle = False
for line in lines:
    if not reached_middle and line != "":
        rules.append(line)
    
    if reached_middle and line != "":
        updates.append(line)
        
    if line == "":
        reached_middle = True
        
before_map = {}
for rule in rules:
    page, before = rule.split("|")
    if page not in before_map:
        before_map[page] = [before]
    else:
        before_map[page].append(before)
        if before not in before_map:
            before_map[before] = []

# --- Part 1 ---

def well_ordered_update(update: list[str]) -> bool:
    # Check each element in the update
    for i in range(len(update) - 1):
        if update[i+1] not in before_map:
            continue
            
        if update[i] in before_map[update[i+1]]:
            return False
    
    # If valid, add middle element
    return True

total = 0        
for update in updates:
    parsed_update = update.split(",")
    if well_ordered_update(parsed_update):
        total += int(parsed_update[len(parsed_update) // 2])

print(f"Part 1: {total}")

# --- Part 2 ---        

total = 0        
for update in updates:
    parsed_update = update.split(",")
    if not well_ordered_update(parsed_update):
        
        # Then we need to order parsed_update based on before_map dictionary
        # We have to perform topological sort with DFS
        ordered = []
        temp = set()
        perm = set()
        
        def visit(node):
            if node in perm or node not in parsed_update:
                return False
            if node in temp:
                return True
            
            temp.add(node)
            for neighbor in before_map[node]:
                if visit(neighbor):
                    return True
            temp.remove(node)
            perm.add(node)
            ordered.append(node)
            return False
        
        while len(ordered) < len(parsed_update):
            for node in parsed_update:
                if visit(node):
                    break
                
        print(ordered)
        total += int(ordered[len(ordered) // 2])
                
print(f"Part 2: {total}")