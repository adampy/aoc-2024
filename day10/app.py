f = open("day10/input.txt", "r")
lines = [l.strip() for l in f.readlines()]
f.close()

# --- Part 1 ---

def get_trailhead_score(start, x, y, uniques=None) -> tuple[int, set[tuple[int, int]] | None]:
    if uniques is None:
        if start == 9 and lines[y][x] == "9":
            return 1, None
    else:
        if start == 9 and lines[y][x] == "9" and (x, y) not in uniques:
            uniques.add((x, y))
            return 1, uniques
    
    if lines[y][x] != str(start):
        return 0, uniques
    
    # Check each surrounding cell for start + 1 and then add trailhead score for that cell to overall score
    score = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            # If in centre of grid, or in corner, or out of bounds skip
            if (dx == 0 and dy == 0) or \
                (dx == -1 and dy == -1) or \
                (dx == -1 and dy == 1) or \
                (dx == 1 and dy == -1) or \
                (dx == 1 and dy == 1) or \
                (x + dx >= len(lines[0]) or y + dy >= len(lines)) or \
                (x + dx < 0 or y + dy < 0):
                continue
            
            #print(f"{' '*start}At {x}, {y} checking {x + dx}, {y + dy} for {start + 1}")
            if lines[y + dy][x + dx] == str(start + 1):
                #print(f"{' '*start}Found it!")
                sc, un = get_trailhead_score(start + 1, x + dx, y + dy, uniques)
                score += sc
                if un is not None and uniques is not None:
                    uniques.update(un)
                #print(f"{' '*start}Score is now {score}")
    return score, uniques

scores = []
for y, line in enumerate(lines):
    score_line = []
    for x, c in enumerate(line):
        score = 0
        if c != ".":
            score, uniques = get_trailhead_score(0, x, y, set())
        score_line.append(score)
    scores.append(score_line)
    
print(f"Part 1: {sum([sum(score_line) for score_line in scores])}")

# --- Part 2 ---

scores = []
for y, line in enumerate(lines):
    score_line = []
    for x, c in enumerate(line):
        score = 0
        if c != ".":
            score, uniques = get_trailhead_score(0, x, y, None)
        score_line.append(score)
    scores.append(score_line)
    
print(f"Part 1: {sum([sum(score_line) for score_line in scores])}")