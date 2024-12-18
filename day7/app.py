import itertools

f = open("day7/input.txt", "r")
lines = [l.strip() for l in f.readlines()]
f.close()

for i in range(len(lines)):
    parts = lines[i].split(": ")
    res = parts[0]
    nums = parts[1].split(" ")
    lines[i] = int(res), [int(x) for x in nums]

# --- Part 1 ---

def can_make_valid(line):
    res, nums = line
    n = len(nums) - 1
    possible_operations = [''.join(p) for p in itertools.product('+*', repeat=n)]
    
    for ops in possible_operations:
        result = nums[0]
        i = 1
        for op in ops:
            if op == "+":
                result += nums[i]
            else:
                result *= nums[i]
            i += 1
        if result == res:
            return result
    return 0

total = 0
for line in lines:
    total += can_make_valid(line)
        
print(f"Part 1: {total}")

# --- Part 2 ---

def can_make_valid_with_concat(line):
    res, nums = line
    n = len(nums) - 1
    possible_operations = [''.join(p) for p in itertools.product('+*|', repeat=n)]
    
    for ops in possible_operations:
        result = nums[0]
        i = 1
        for op in ops:
            if op == "+":
                result += nums[i]
            elif op == "*":
                result *= nums[i]
            else:
                result = int(str(result) + str(nums[i]))
            i += 1
        
        if result == res:
            return result
    return 0

total = 0
for line in lines:
    total += can_make_valid_with_concat(line)
        
print(f"Part 2: {total}")