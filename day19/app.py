import functools

f = open("day19/input.txt", "r")
towels, patterns = f.read().split("\n\n")
towels = towels.replace(" ", "").split(",")
patterns = patterns.split("\n")
f.close()

# --- Part 1 ---

# Returns a list of patterns used to make the pattern, or None if cannot be made
def make_pattern(pattern: str) -> list[str] | None:
    if pattern == "":
        return []
    
    for p in towels:
        if pattern.startswith(p):
            used = make_pattern(pattern[len(p):])
            if used is None:
                continue
            return [p] + used
    return None

possible = 0
for pattern in patterns:
    used = make_pattern(pattern)
    #print("Pattern:", pattern, "Used:", used)
    if used is not None:
        possible += 1

print(f"Part 1: {possible}")

# --- Part 2 ---

# Returns a count of how many ways the pattern can be created, or 0 if cannot be made
@functools.lru_cache
def make_pattern_count(pattern: str) -> int:
    if pattern == "":
        return 0
    
    count = 0
    for p in towels:
        if pattern == p:
            count += 1
        
        if pattern.startswith(p):
            used = make_pattern_count(pattern[len(p):])
            count += used
    return count

total_count = 0
for pattern in patterns:
    total_count += make_pattern_count(pattern)
print(f"Part 2: {total_count}")