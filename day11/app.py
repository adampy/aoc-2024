import functools

f = open("day11/input.txt", "r")
lines = [line.strip() for line in f.readlines()]
f.close()
orig_stones = [int(i) for i in lines[0].split(" ")]

# --- Part 1 ---

def blink(stones):
    i = 0
    while i < len(stones):
        str_stone = str(stones[i])   
        
        res = []
        
        if stones[i] == 0:
            stones[i] = 1
            res.append(1)
        elif len(str_stone) % 2 == 0:
            # Make new stone with half of the number engraved on this stone
            stones.insert(i, int(str_stone[:len(str_stone)//2]))
            stones[i+1] = int(str_stone[len(str_stone)//2:])
            
            res.append(stones[i])
            res.append(stones[i+1])
            i += 1
        else:
            stones[i] *= 2024
            res.append(stones[i])
        i += 1
    return stones

n = 25
stones = orig_stones.copy()
for i in range(n):
    print("blink ", i, len(stones))
    stones = blink(stones)
print("Part 1:", len(stones))

# --- Part 2 ---

@functools.cache
def new_blink(stone: int, depth: int) -> int:
    if depth == 0:
        return 1
    if stone == 0:
        return new_blink(1, depth - 1)
    elif len(str(stone)) % 2 == 0:
        first_half = str(stone)[:len(str(stone)) // 2]
        second_half = str(stone)[len(str(stone)) // 2:]
        return new_blink(int(first_half), depth - 1) + new_blink(int(second_half), depth - 1)
    else:
        return new_blink(stone * 2024, depth - 1)

total = 0
for stone in orig_stones:
    total += new_blink(stone, 75)
print(f"Part 2: {total}")