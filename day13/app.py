import re
from dataclasses import dataclass
import numpy as np
from math import isclose

f = open("day13/input.txt", "r")
lines = f.read()
f.close()
unparsed = lines.split("\n\n")

# --- Part 1 ---

@dataclass
class Machine:
    buttonAX: int
    buttonAY: int
    buttonBX: int
    buttonBY: int
    prizeX: int
    prizeY: int

# Match all digits (\d+)
machines = []
for machine in unparsed:
    matches = re.findall(r'\d+', machine)
    machines.append(Machine(*[int(x) for x in matches]))

def solve(machine: Machine, limit: int = 100) -> int:
    # Formulate as simultaneous equations
    A = [[machine.buttonAX, machine.buttonBX], [machine.buttonAY, machine.buttonBY]]
    Y = [machine.prizeX, machine.prizeY]
    res = np.linalg.solve(A, Y)
    
    # (Dis)allowed conditions
    if res[0] < 0 or res[1] < 0:
        return 0
    elif limit != 0 and (res[0] > limit or res[1] > limit):
        return 0
    else:
        rounded = [round(res[0]), round(res[1])]
        calcPrizeX = machine.buttonAX * rounded[0] + machine.buttonBX * rounded[1]
        calcPrizeY = machine.buttonAY * rounded[0] + machine.buttonBY * rounded[1]
        if calcPrizeX != machine.prizeX or calcPrizeY != machine.prizeY:
            return 0
        else:
            # Allowed condition
            cost = 3 * rounded[0] + rounded[1]
            return cost

total = 0
for machine in machines:
    total += solve(machine)
print(f"Part 1: {total}")

# --- Part 2 ---
total = 0
for machine in machines:
    machine.prizeX += 10000000000000
    machine.prizeY += 10000000000000
    total += solve(machine, 0)
print(f"Part 2: {total}")