import re

# --- Part One ---

combined_data = ""
with open("day3/input.txt") as f:
    for line in f:
        combined_data += line

groups = re.findall(r"(mul\(\d{1,3},\d{1,3}\))", combined_data)

total = 0
for group in groups:
    num1, num2 = re.findall(r"(\d+)", group)
    total += int(num1) * int(num2)
    
print(f"Part 1: {total}")

# --- Part Two ---

     
class Token:
    DO = "do()"
    DONT = "don't()"
    MUL = "mul"
    COMMA = ","
    BRACKET_OPEN = "("
    BRACKET_CLOSE = ")"
    NUMBER = "number"

def parse_number(i):
    j = i
    number_seen = False
    while j < len(combined_data) and combined_data[j].isdigit():
        number_seen = True
        j += 1
        
    if number_seen:
        return False, j, int(combined_data[i:j])
    else:
        return True, i, 0

def parse_token(i, token):
    if combined_data[i:i+len(token)] == token:
        return False, i+len(token)
    else:
        return True, i

def parse_mult(i):
    start = i
    error, i = parse_token(i, Token.MUL)
    if error: return True, start, 0
    error, i = parse_token(i, Token.BRACKET_OPEN)
    if error: return True, start, 0
    error, i, num1 = parse_number(i)
    if error: return True, start, 0
    error, i = parse_token(i, Token.COMMA)
    if error: return True, start, 0
    error, i, num2 = parse_number(i)
    if error: return True, start, 0
    error, i = parse_token(i, Token.BRACKET_CLOSE)
    if error: return True, start, 0
    return False, i, num1 * num2
    
i = 0
enabled = True
parsing_mult = False
total = 0
while (i < len(combined_data)):
    # Parsing do
    error, i = parse_token(i, Token.DO)
    if error is False:
        enabled = True
        continue
    
    # Parsing don't
    error, i = parse_token(i, Token.DONT)
    if error is False:
        enabled = False
        continue
    
    # Parsing mult
    error, i, result = parse_mult(i)
    if error is False:
        if enabled:
            total += result
        continue
    
    # else
    i += 1
    
print(f"Part 2: {total}")