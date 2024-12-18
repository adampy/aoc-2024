f = open("day9/input.txt", "r")
line = f.readline().strip()
f.close()


class Block:
    def __init__(self, num, block):
        self.num = num
        self.block = block
        self.has_moved = False

    def is_free(self):
        return self.block == "."
    
    def __str__(self):
        return f"{self.num} * {self.block}"
    
    def __repr__(self):
        return f"{self}"

def expand_to_blocks(line):
    blocks = []
    current_block = 0
    for i in range(len(line)):
        num = int(line[i])
        if i % 2 == 0:
            # Parsing number of positions in block
            blocks.append(Block(num, str(current_block)))
            current_block += 1
        else:
            # Parsing free spaces between blocks
            blocks.append(Block(num, "."))
            
    # Remove any blocks with 0 length
    i = 0
    while i < len(blocks):
        if blocks[i].num == 0:
            blocks.pop(i)
        else:
            i += 1
            
    
    return blocks

def condense(blocks):
    front = 0
    back = len(blocks) - 1
    
    while front < back:
        fb = blocks[front]
        bb = blocks[back]
        
        # Ignore non-free space
        if not fb.is_free():
            front += 1
        
        # We need to get back to something that is not free space
        elif bb.is_free():
            blocks.pop(back)
            back -= 1
            
        # We can add to front block, which is free        
        elif not bb.is_free():              
            # If we have free space left over then we need to create a new block after front
            if fb.num > bb.num:
                fb.block = bb.block
                blocks.insert(front + 1, Block(fb.num - bb.num, "."))
                fb.num = bb.num
                blocks.pop(back + 1)
                front += 1
            # Else we have just enough room, so we can remove back block
            elif fb.num == bb.num:
                fb.block = bb.block
                front += 1
                blocks.pop(back)
                back -= 1
            # If we can only move part of back block
            else:
                fb.block = bb.block
                bb.num -= fb.num
                front += 1
    
    return blocks
    
def checksum(blocks):
    num = 0
    
    i = 0
    while len(blocks):
        b = blocks.pop(0)
        for j in range(b.num):
            if not b.is_free():
                num += int(b.block) * (i + j)
        i += j + 1
            
    return num

# --- Part 1 ---
expansion = expand_to_blocks(line)
condensed = condense(expansion)
num = checksum(condensed)
print(f"Part 1: {num}")

# --- Part 2 ---
def condense_new(blocks):
    
    i = len(blocks) - 1
    while i > 0:
        if blocks[i].has_moved or blocks[i].is_free():
            i -= 1
            continue
        
        bb = blocks[i]
        moved = False
        for j in range(i):
            sb = blocks[j]
            if sb.is_free():
                if sb.num == bb.num:
                    sb.block = bb.block
                    sb.has_moved = True
                    bb.block = "."
                    i -= 1
                    moved = True
                    break
                elif sb.num > bb.num:
                    sb.block = blocks[i].block
                    blocks.insert(j + 1, Block(sb.num - bb.num, "."))
                    sb.has_moved = True
                    sb.num = bb.num
                    bb.block = "."
                    moved = True
                    break
        if not moved:
            i -= 1
            
        #print("".join([b.block * b.num for b in blocks]))
    
    return blocks

expansion = expand_to_blocks(line)
condensed = condense_new(expansion)
num = checksum(condensed)
print(f"Part 2: {num}")