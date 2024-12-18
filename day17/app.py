f = open("day17/input.txt", "r")
registers, program = f.read().split("\n\n")
f.close()
registers = [int(r[12:]) for r in registers.split("\n")]
program = [int(p) for p in program[9:].split(",")]

# --- Part 1 ---

class Opcode:
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7
    
def print_registers(registers):
    print("Register A:", registers[0])
    print("Register B:", registers[1])
    print("Register C:", registers[2])
    
def get_combo_operand(ip, registers, program):
    operand = program[ip]
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registers[0]
    elif operand == 5:
        return registers[1]
    elif operand == 6:
        return registers[2]
    elif operand == 7:
        raise Exception("Invalid operand")

def run(registers, program) -> list[str]:
    ip = 0 # instruction pointer
    outputs = []
    
    while ip < len(program):
        opcode = program[ip]
        ip += 1
        
        if opcode == Opcode.adv or opcode == Opcode.bdv or opcode == Opcode.cdv:
            if ip >= len(program): break
            numerator = registers[0]
            denominator = 2 ** get_combo_operand(ip, registers, program)
            ip += 1
            result = int(numerator / denominator)
            if opcode == Opcode.adv:
                registers[0] = result
            elif opcode == Opcode.bdv:
                registers[1] = result
            elif opcode == Opcode.cdv:
                registers[2] = result
        
        elif opcode == Opcode.bxl:
            if ip >= len(program): break
            registers[1] = registers[1] ^ program[ip]
            ip += 1
            
        elif opcode == Opcode.bst:
            if ip >= len(program): break
            registers[1] = get_combo_operand(ip, registers, program) % 8
            ip += 1
            
        elif opcode == Opcode.jnz:
            if registers[0] == 0: continue
            if ip >= len(program): break
            ip = program[ip]
            
        elif opcode == Opcode.bxc:
            if ip >= len(program): break
            registers[1] = registers[1] ^ registers[2]
            ip += 1
            
        elif opcode == Opcode.out:
            if ip >= len(program): break
            output = get_combo_operand(ip, registers, program) % 8
            ip += 1
            outputs.append(output)
    
    return outputs

outputs = run(registers, program)
print(f"Part 1: {','.join([str(o) for o in outputs])}")

# --- Part 2 ---

# 2,4   1,3   7,5   0,3   1,5   4,4   5,5   3,0
# 0: B = A
# 2: B = B ^ 3
# 4: C = A / 2**B
# 6: A = A / 2**3
# 8: 

# bst 4      B = A % 8
# bxl 3      B = B ^ 3
# cdv 5      C = A // 2**B
# adv 3      A = A // 2**3
# bxl 5      B = B ^ 5
# bxc 4      B = B ^ C
# out 5      output = B % 8
# jnz        repeat above if A != 0
# adv HALT

def step(A, B, C):
    B = A % 8
    B = B ^ 3
    C = A // 2**B
    A = A // 2**3
    B = B ^ 5
    B = B ^ C
    output = B % 8
    return A, B, C, output

def run2(A):
    B = 0
    C = 0
    
    outputs = []
    while A != 0:
        A, B, C, output = step(A, B, C)
        outputs.append(output)
    return outputs

def find(A, col=0):
    if step(A, 0, 0)[3] != program[-(col + 1)]:
        return

    if col == len(program) - 1:
        As.append(A)
    else:
        for B in range(8):
            find(A * 8 + B, col + 1)
            
As = []
for a in range(8):
    find(a)
print(f"Part 2: {As[0]}")